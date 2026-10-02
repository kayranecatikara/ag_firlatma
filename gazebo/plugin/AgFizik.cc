// AgFizik.cc — Gazebo Harmonic (gz-sim 8) system plugin
//
// Ag fizigi: netfull.py'daki DOGRULANMIS modeli Gazebo'ya tasir.
//   * iplikler yalnizca CEKME tasir (tension-only viskoelastik)
//   * her eleman icin NORMAL/TEGET ayrisimli silindir suruklemesi
//   * kaba orgu gercek agi temsil eder -> surukleme olcek faktoru
//   * serbest akis (drone hava hizi) rüzgar olarak verilir
//   * t=firlatma_t aninda bilyelere + dugumlere baslangic hizi verilir
//
// Gazebo'nun katkisi: temas/dolanma, carpisma, gorsellestirme.
// Ag ici kuvvetleri BU plugin hesaplar (SDF eklemleri tension-only yapamaz).
//
// SDF parametreleri <plugin> altinda:
//   <dugum_on_ek>   dugum linklerinin ad oneki (orn. "dugum_")
//   <bilye_on_ek>   bilye linklerinin ad oneki (orn. "bilye_")
//   <eleman>        her biri "i j L0" (dugum indisleri + serbest boy [m])
//   <EA>            iplik eksenel rijitlik [N]   (E*A, olceklenmis)
//   <zeta>          iplik sonumleme orani (0..1)
//   <d_iplik>       iplik capi [m]
//   <Cdn> <Cdt>     normal / teget surukleme katsayilari
//   <aero_olcek>    kaba orgu -> gercek ag surukleme olcegi (L_gercek/L_kaba)
//   <rho>           hava yogunlugu
//   <ruzgar>        "x y z" serbest akis hizi [m/s] (drone cercevesinde)
//   <bilye_Cd> <bilye_D>  bilye surukleme
//   <bilye_indis>   bilye olan DUGUM indisleri, bosluklu liste (kure suruklemesi)
//   <log_dosya>     CSV kayit yolu (bos = kapali)
//   <log_dt>        kayit araligi [s]
//   <firlatma_t>    atis ani [s].  <=0 ise ZAMANA GOMULU ATIS YOK;
//                   yalnizca DISARIDAN tetiklenir (bkz. <tetik_konu>).
//   <tetik_konu>    Gazebo topic adi (gz.msgs.Boolean). Bu konuya true
//                   gelince ag firlatilir. Varsayilan: /ag_firlatici/ates
//                     gz topic -t /ag_firlatici/ates -m gz.msgs.Boolean -p "data: true"
//   <firlatici_link>  Firlaticinin TASIYICI LINK adi (orn. "namlu").
//                   Verilirse:
//                     * atis ONCESINDE ag dugumleri bu linke KINEMATIK
//                       OLARAK TASINIR (drone ucarken ag onunla gider)
//                     * atis aninda hizlar linkin O ANKI YONELIMINE gore
//                       uygulanir (dunya eksenine gore DEGIL)
//                   Verilmezse eski davranis: dunya +X yonune firlatir.
//   <uretim_firlatici_poz>  "x y z roll pitch yaw" -- ag dugum pozlarinin
//                   URETILIRKEN varsayilan firlatici pozu. Dugum pozlari
//                   SDF'te MUTLAK yazilidir; bu alan sayesinde plugin
//                   onlari firlaticinin GERCEK pozuna tasiyabilir.
//                   Boylece firlaticiyi dunyada ISTEDIGIN YERE koyabilirsin.
//                   Verilmezse dugumler bulunduklari yerde kabul edilir.
//   <v_eksenel>     namlu cikis hizi [m/s] (+X yonunde)
//   <v_radyal>      bilyelerin radyal acilma hizi [m/s]

#include <gz/plugin/Register.hh>
#include <gz/transport/Node.hh>
#include <gz/msgs/boolean.pb.h>
#include <gz/sim/System.hh>
#include <gz/sim/Link.hh>
#include <gz/sim/Model.hh>
#include <gz/sim/Util.hh>
#include <gz/sim/components/AngularVelocityCmd.hh>
#include <gz/sim/components/LinearVelocityCmd.hh>
#include <gz/sim/components/Inertial.hh>
#include <gz/sim/components/Link.hh>
#include <gz/sim/components/Name.hh>
#include <gz/sim/components/ParentEntity.hh>
#include <gz/sim/components/Pose.hh>
#include <gz/sim/components/PoseCmd.hh>
#include <gz/math/Vector3.hh>
#include <sdf/Element.hh>

#include <atomic>
#include <fstream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

namespace ag
{
using namespace gz;
using namespace gz::sim;

struct Eleman { int i, j; double L0; };

class AgFizik : public System,
                public ISystemConfigure,
                public ISystemPreUpdate
{
public:
  void Configure(const Entity &_entity,
                 const std::shared_ptr<const sdf::Element> &_sdf,
                 EntityComponentManager &_ecm, EventManager &) override
  {
    this->dunya = _entity;
    auto sdfp = _sdf->Clone();

    auto getD = [&](const char *k, double d) {
      return sdfp->HasElement(k) ? sdfp->Get<double>(k) : d; };
    auto getS = [&](const char *k, const std::string &d) {
      return sdfp->HasElement(k) ? sdfp->Get<std::string>(k) : d; };

    this->EA        = getD("EA", 100.0);
    this->zeta      = getD("zeta", 0.30);
    this->dIplik    = getD("d_iplik", 1.65e-4);
    this->Cdn       = getD("Cdn", 1.10);
    this->Cdt       = getD("Cdt", 0.03);
    this->aeroOlcek = getD("aero_olcek", 1.0);
    this->rho       = getD("rho", 1.225);
    this->bilyeCd   = getD("bilye_Cd", 0.47);
    this->bilyeD    = getD("bilye_D", 0.0127);
    this->firlatmaT = getD("firlatma_t", 0.0);
    this->vEks      = getD("v_eksenel", 34.5);
    this->vRad      = getD("v_radyal", 8.0);
    this->logDt     = getD("log_dt", 0.005);
    this->mDugum    = getD("m_dugum", 2.76e-5);   // sonumleme olcegi
    this->Fsinir    = getD("F_sinir", 200.0);     // SADECE sayisal guvenlik
    this->Tkopma    = getD("T_kopma", 64.15);     // lif kopma yuku
    this->Tdugum    = getD("T_dugum", 35.3);      // DUGUMLU ag kopma yuku
    this->pervX     = getD("perv_x", -0.47);
    this->pervR     = getD("perv_r", 0.115);
    this->logYol    = getS("log_dosya", "");
    this->pozYol    = getS("poz_dosya", "");
    this->pozDt     = getD("poz_dt", 0.01);

    if (sdfp->HasElement("hiz"))
      for (auto e = sdfp->GetElement("hiz"); e; e = e->GetNextElement("hiz"))
      {
        std::istringstream ss(e->Get<std::string>());
        int k; double x, y, z;
        if (ss >> k >> x >> y >> z) this->devirHiz[k] = math::Vector3d(x, y, z);
      }
    this->devirT = getD("devir_t", 0.0);

    if (sdfp->HasElement("bilye_indis"))
    {
      std::istringstream ss(sdfp->Get<std::string>("bilye_indis"));
      int k; while (ss >> k) this->bilyeIdx.push_back(k);
    }

    if (sdfp->HasElement("ruzgar"))
    {
      std::istringstream ss(sdfp->Get<std::string>("ruzgar"));
      double x, y, z; ss >> x >> y >> z;
      this->ruzgar = math::Vector3d(x, y, z);
    }

    this->hedefAd = getS("hedef_ad", "");
    this->tetikKonu  = getS("tetik_konu", "/ag_firlatici/ates");
    this->firlaticiAd = getS("firlatici_link", "");
    if (sdfp->HasElement("uretim_firlatici_poz"))
    {
      std::istringstream ss(sdfp->Get<std::string>("uretim_firlatici_poz"));
      double x, y, z, r, p, w;
      if (ss >> x >> y >> z >> r >> p >> w)
      { this->uretimPoz = math::Pose3d(x, y, z, r, p, w);
        this->uretimPozVar = true; }
    }
    this->dugumOn = getS("dugum_on_ek", "dugum_");
    this->bilyeOn = getS("bilye_on_ek", "bilye_");

    // --- elemanlari oku:  "i j L0"
    for (auto e = sdfp->GetElement("eleman"); e; e = e->GetNextElement("eleman"))
    {
      std::istringstream ss(e->Get<std::string>());
      Eleman el; ss >> el.i >> el.j >> el.L0;
      if (el.L0 > 1e-9) this->elemanlar.push_back(el);
    }
    // --- DISARIDAN TETIKLEME
    if (!this->tetikKonu.empty())
    {
      this->dugum.Subscribe(this->tetikKonu, &AgFizik::TetikGeldi, this);
      gzmsg << "[AgFizik] tetik konusu: " << this->tetikKonu
            << "  (gz topic -t " << this->tetikKonu
            << " -m gz.msgs.Boolean -p \"data: true\")\n";
    }
    gzmsg << "[AgFizik] yuklendi: " << this->elemanlar.size() << " eleman, "
          << (this->firlatmaT > 0
                ? "zamanli atis t=" + std::to_string(this->firlatmaT) + "s"
                : std::string("atis YALNIZCA disaridan tetiklenir"))
          << (this->firlaticiAd.empty() ? "" : ", firlatici=" + this->firlaticiAd)
          << "\n";
  }

  // Dunya seviyesindeki plugin Configure'da calistiginda modeller HENUZ
  // OLUSMAMIS olur; bu yuzden link kesfi ilk PreUpdate'te yapilir.
  // Her dugum AYRI MODEL olmali: tek model icindeki eklemsiz linkleri
  // gz-physics/DART tek govdeye kaynaklar ve hicbiri hareket etmez.
  void Kesfet(EntityComponentManager &_ecm)
  {
    std::map<int, Entity> dugumMap, bilyeMap;
    _ecm.Each<components::Link, components::Name>(
      [&](const Entity &lE, const components::Link *,
          const components::Name *nm) -> bool
      {
        const std::string &ad = nm->Data();
        auto al = [&](const std::string &on, std::map<int, Entity> &m) {
          if (!on.empty() && ad.rfind(on, 0) == 0) {
            try { m[std::stoi(ad.substr(on.size()))] = lE; } catch (...) {}
            return true; }
          return false; };
        if (!this->hedefAd.empty() && ad == this->hedefAd) this->hedef = lE;
        if (!this->firlaticiAd.empty() && ad == this->firlaticiAd)
          this->firlatici = lE;
        if (!al(this->dugumOn, dugumMap)) al(this->bilyeOn, bilyeMap);
        return true;
      });
    if (dugumMap.empty()) return;          // henuz olusmadi, sonraki adimda dene

    int nMax = -1;
    for (auto &kv : dugumMap) nMax = std::max(nMax, kv.first);
    this->dugumlar.assign(nMax + 1, kNullEntity);
    for (auto &kv : dugumMap) this->dugumlar[kv.first] = kv.second;
    for (auto &kv : bilyeMap) this->bilyeler.push_back(kv.second);
    // <bilye_indis> ile verilen dugumler de bilye sayilir (kure suruklemesi)
    for (int k : this->bilyeIdx)
      if (k >= 0 && k < (int)this->dugumlar.size() &&
          this->dugumlar[k] != kNullEntity)
        this->bilyeler.push_back(this->dugumlar[k]);

    // hiz/ivme bilesenlerini etkinlestir
    for (auto e : this->dugumlar)
      if (e != kNullEntity) { Link(e).EnableVelocityChecks(_ecm, true); }
    for (auto e : this->bilyeler) Link(e).EnableVelocityChecks(_ecm, true);
    if (this->hedef != kNullEntity)
    {
      Link(this->hedef).EnableVelocityChecks(_ecm, true);
      auto hp = Link(this->hedef).WorldPose(_ecm);
      if (hp) this->hedefP0 = hp->Pos();
      // Hedef SEYIR HALINDE: tasima yercekimini dengeler. Trim kuvveti
      // uygulamazsak serbest duser ve hedef_dx agin etkisini DEGIL dusmeyi
      // olcer. m*g'yi yukari uygulayip hedefi trimli birakiyoruz.
      auto in = _ecm.Component<components::Inertial>(this->hedef);
      if (in) this->hedefM = in->Data().MassMatrix().Mass();
      gzmsg << "[AgFizik] hedef kutlesi " << this->hedefM << " kg, trim acik\n";
      gzmsg << "[AgFizik] hedef bulundu: " << this->hedefAd
            << " @ x=" << this->hedefP0.X() << "\n";
    }

    if (this->firlatici != kNullEntity)
    {
      Link(this->firlatici).EnableVelocityChecks(_ecm, true);
      auto fp = Link(this->firlatici).WorldPose(_ecm);
      if (fp) this->firlaticiP0 = *fp;
      gzmsg << "[AgFizik] firlatici link bulundu: " << this->firlaticiAd
            << " — ag atisa kadar KINEMATIK TASINACAK\n";
    }
    else if (!this->firlaticiAd.empty())
      gzwarn << "[AgFizik] firlatici link '" << this->firlaticiAd
             << "' BULUNAMADI — ag dunya eksenine gore firlatilacak\n";

    if (!this->logYol.empty())
    {
      this->log.open(this->logYol);
      this->log << "t,R_bilye,X_bilye,X_merkez,R_std,T_max,v_bilye,F_max,kirpma,"
                   "hedef_dx,hedef_v,n_gecen,n_sarma,n_kopan,"
                   "n50,n75,n100,n_perv,n_perv_toplam\n";
    }
    if (!this->pozYol.empty())
    {
      this->pozLog.open(this->pozYol);
      // basligin ilk satiri: dugum sayisi + eleman listesi (cizim icin)
      this->pozLog << "# n_dugum " << this->dugumlar.size() << "\n";
      for (const auto &el : this->elemanlar)
        this->pozLog << "# e " << el.i << " " << el.j << "\n";
    }
    gzmsg << "[AgFizik] KESIF: " << dugumMap.size() << " dugum, "
          << this->bilyeler.size() << " bilye, " << this->elemanlar.size()
          << " eleman, aero_olcek=" << this->aeroOlcek << "\n";
    this->kesfedildi = true;
  }

  void PreUpdate(const UpdateInfo &_info, EntityComponentManager &_ecm) override
  {
    if (_info.paused) return;
    if (!this->kesfedildi) { this->Kesfet(_ecm); return; }
    const double t = std::chrono::duration<double>(_info.simTime).count();

    // Hedef SEYIR HALINDE: tasima = agirlik. Trimi ATIS ONCESINDE DE
    // uygulamazsak hedef bekleme suresi boyunca serbest duser ve olcum
    // kirlenir (0.02 s bekleme -> 0.2 m/s sahte hiz).
    this->HedefTrim(_ecm);

    // ---------- FIRLATMA: bilyelere ve dugumlere baslangic hizi ----------
    // ---------- ATIS ONCESI: agi firlaticiyla birlikte TASI ----------
    // Drone ucarken ag onunla gitmeli. Dugumler serbest <model>'ler
    // oldugu icin, atisa kadar poz komutuyla firlaticiya kilitlenirler.
    if (!this->atildi && this->firlatici != kNullEntity)
      this->AgiTasi(_ecm);

    const bool zamanli = (this->firlatmaT > 0.0 && t >= this->firlatmaT);
    if (!this->atildi && (zamanli || this->tetikIstendi.load()))
    {
      this->atildi = true;
      // ONEMLI: poz komutu AYNI ADIMDA kaldirilmali. Bir adim beklersek
      // WorldPoseCmd ile SetLinearVelocity ayni adimda CAKISIR; dugumler
      // once poza kilitlenip sonra serbest kalir ve ag sahte bir gerilme
      // sicramasi yasar (olculdu: tepe gerilme 16 -> 31 N).
      for (auto e : this->dugumlar)
        if (e != kNullEntity) _ecm.RemoveComponent<components::WorldPoseCmd>(e);
      auto merkez = this->OrtaKonum(_ecm);
      // PYTHON MODELIYLE AYNI: eksenel hiz TUM dugumlere, radyal acilma
      // hizi YALNIZCA bilyelere (agi onlar cekip acar).
      std::vector<bool> bilyeMi(this->dugumlar.size(), false);
      for (int k : this->bilyeIdx)
        if (k >= 0 && k < (int)bilyeMi.size()) bilyeMi[k] = true;

      for (size_t k = 0; k < this->dugumlar.size(); ++k)
      {
        if (this->dugumlar[k] == kNullEntity) continue;
        Link L(this->dugumlar[k]);
        auto p = L.WorldPose(_ecm);
        if (!p) continue;
        math::Vector3d v;
        auto it = this->devirHiz.find((int)k);
        if (it != this->devirHiz.end())
        {
          v = it->second;                 // HIBRIT: Python'dan devralinan hiz
        }
        else
        {
          v = math::Vector3d(this->vEks, 0, 0);
          if (bilyeMi[k])
          {
            math::Vector3d r = p->Pos() - merkez; r.X() = 0;
            double rn = r.Length();
            if (rn > 1e-6) v += r / rn * this->vRad;
          }
        }
        // FIRLATICI CERCEVESI: hizlar namlunun O ANKI yonelimine gore
        // dondurulur; ayrica firlaticinin kendi hizi eklenir (drone
        // ucuyorsa ag onun hiziyla birlikte cikar).
        if (this->firlatici != kNullEntity)
        {
          auto fp = Link(this->firlatici).WorldPose(_ecm);
          if (fp) v = fp->Rot().RotateVector(v);
          auto fv = Link(this->firlatici).WorldLinearVelocity(_ecm);
          if (fv) v += *fv;
        }
        L.SetLinearVelocity(_ecm, v);
      }
      if (this->devirHiz.empty())
        gzmsg << "[AgFizik] ATIS! t=" << t << "s  v_eks=" << this->vEks
              << " v_rad=" << this->vRad << "\n";
      else
        gzmsg << "[AgFizik] DEVIR! t=" << t << "s, Python t="
              << this->devirT << "s, " << this->devirHiz.size()
              << " dugum hizi devralindi\n";
      return;   // ayni adimda kuvvet uygulama
    }
    if (!this->atildi) return;

    // ONEMLI: SetLinearVelocity kalici bir KINEMATIK KISIT birakir
    // (LinearVelocityCmd her adimda yeniden uygulanir) -> govde o hiza
    // kilitlenir ve hicbir kuvvet etki etmez. Atistan bir adim sonra
    // komutu kaldirip govdeleri SERBEST birakiyoruz.
    if (!this->cmdTemizlendi)
    {
      this->cmdTemizlendi = true;
      auto temizle = [&](Entity e) {
        if (e == kNullEntity) return;
        _ecm.RemoveComponent<components::LinearVelocityCmd>(e);
        _ecm.RemoveComponent<components::AngularVelocityCmd>(e);
        // WorldPoseCmd de KALICI KINEMATIK KISITTIR -- tasima bittiginde
        // kaldirilmazsa dugumler firlaticiya kilitli kalir.
        _ecm.RemoveComponent<components::WorldPoseCmd>(e); };
      for (auto e : this->dugumlar) temizle(e);
      for (auto e : this->bilyeler) temizle(e);
      gzmsg << "[AgFizik] hiz komutlari kaldirildi, govdeler serbest\n";
    }

    // ---------- durum oku ----------
    const size_t N = this->dugumlar.size();
    std::vector<math::Vector3d> P(N), V(N);
    std::vector<bool> ok(N, false);
    for (size_t k = 0; k < N; ++k)
    {
      if (this->dugumlar[k] == kNullEntity) continue;
      Link L(this->dugumlar[k]);
      auto p = L.WorldPose(_ecm);
      auto v = L.WorldLinearVelocity(_ecm);
      if (!p || !v) continue;
      if (!p->Pos().IsFinite() || !v->IsFinite() ||
          p->Pos().Length() > 1e3 || v->Length() > 1e4)
      {
        if (!this->iraksadi)
        {
          this->iraksadi = true;
          gzerr << "[AgFizik] IRAKSAMA! dugum " << k
                << "  |P|=" << p->Pos().Length()
                << "  |v|=" << v->Length() << "  t=" << t
                << "  -> dt kucultun (su an iplik periyodu/15 onerilir)\n";
        }
        continue;
      }
      P[k] = p->Pos(); V[k] = *v; ok[k] = true;
    }
    if (this->iraksadi) return;   // bozulmus duruma kuvvet uygulamayalim

    std::vector<math::Vector3d> F(N, math::Vector3d::Zero);
    int n50 = 0, n75 = 0, n100 = 0;   // bu adimda zorlanan eleman sayilari

    // ---------- iplik elemanlari: CEKME-ONLY + eleman aerodinamigi ----------
    for (const auto &el : this->elemanlar)
    {
      if (el.i < 0 || el.j < 0 || (size_t)el.i >= N || (size_t)el.j >= N) continue;
      if (!ok[el.i] || !ok[el.j]) continue;

      math::Vector3d d = P[el.j] - P[el.i];
      double L = d.Length();
      if (L < 1e-9) continue;
      math::Vector3d u = d / L;

      // --- gerilme: yalnizca uzama varken
      if (L > el.L0)
      {
        double k = this->EA / el.L0;
        double c = this->zeta * 2.0 * std::sqrt(k * this->mDugum);
        double Ldot = (V[el.j] - V[el.i]).Dot(u);
        double T = k * (L - el.L0) + c * Ldot;
        if (T > 0.0) { F[el.i] += u * T; F[el.j] -= u * T;
                       this->Tmax = std::max(this->Tmax, T);
                       this->Tzirve = std::max(this->Tzirve, T);
                       if (T > this->Tkopma) ++this->nKopan;
                       if (T > 0.50 * this->Tdugum) ++n50;
                       if (T > 0.75 * this->Tdugum) ++n75;
                       if (T > 1.00 * this->Tdugum) ++n100; }
      }

      // --- aerodinamik: normal/teget ayrisimli silindir suruklemesi
      math::Vector3d vm = (V[el.i] + V[el.j]) * 0.5 - this->ruzgar;
      math::Vector3d vt = u * vm.Dot(u);
      math::Vector3d vn = vm - vt;
      double q = 0.5 * this->rho * this->dIplik * L * this->aeroOlcek;
      math::Vector3d Fa = -(vn * (q * this->Cdn * vn.Length()))
                          - (vt * (q * this->Cdt * vt.Length()));
      F[el.i] += Fa * 0.5; F[el.j] += Fa * 0.5;
    }

    this->n50max = std::max(this->n50max, n50);
    this->n75max = std::max(this->n75max, n75);
    this->n100max = std::max(this->n100max, n100);

    for (size_t k = 0; k < N; ++k)
    {
      if (!ok[k] || !F[k].IsFinite()) continue;
      double f = F[k].Length();
      this->Fmax = std::max(this->Fmax, f);
      // guvenlik tavani: sayisal bir sicrama tum kosuyu patlatmasin
      if (f > this->Fsinir) { F[k] *= this->Fsinir / f; ++this->nKirpma; }
      Link(this->dugumlar[k]).AddWorldForce(_ecm, F[k]);
    }

    // ---------- bilye kure suruklemesi ----------
    const double Ab = M_PI * 0.25 * this->bilyeD * this->bilyeD;
    for (auto be : this->bilyeler)
    {
      Link L(be);
      auto v = L.WorldLinearVelocity(_ecm);
      if (!v) continue;
      math::Vector3d vr = *v - this->ruzgar;
      double s = vr.Length();
      if (s < 1e-9) continue;
      math::Vector3d Fd = -vr * (0.5 * this->rho * this->bilyeCd * Ab * s);
      if (Fd.IsFinite()) L.AddWorldForce(_ecm, Fd);
    }

    // ---------- kayit ----------
    if (this->log.is_open() && t >= this->sonLog + this->logDt)
    {
      this->sonLog = t;
      math::Vector3d mrk = math::Vector3d::Zero; int nm2 = 0;
      for (size_t k = 0; k < N; ++k) if (ok[k]) { mrk += P[k]; ++nm2; }
      if (nm2) mrk /= nm2;
      double sR = 0, sR2 = 0, sX = 0, sV = 0; int n = 0;
      for (int k : this->bilyeIdx)
      {
        if (k < 0 || (size_t)k >= N || !ok[k]) continue;
        double r = std::hypot(P[k].Y() - mrk.Y(), P[k].Z() - mrk.Z());
        sR += r; sR2 += r * r; sX += P[k].X(); sV += V[k].X(); ++n;
      }
      double sXc = 0; int nc = 0;
      for (size_t k = 0; k < N; ++k) if (ok[k]) { sXc += P[k].X(); ++nc; }

      // --- HEDEF olculeri
      double hdx = 0.0, hv = 0.0; int nGecen = 0, nSarma = 0, nPerv = 0;
      if (this->hedef != kNullEntity)
      {
        Link HL(this->hedef);
        auto hp = HL.WorldPose(_ecm); auto hvv = HL.WorldLinearVelocity(_ecm);
        if (hp) hdx = (hp->Pos() - this->hedefP0).Length();
        if (hvv) hv = hvv->Length();
        const double xh = hp ? hp->Pos().X() : 0.0;
        const double yh = hp ? hp->Pos().Y() : 0.0;
        const double zh = hp ? hp->Pos().Z() : 0.0;
        for (size_t k = 0; k < N; ++k)
        {
          if (!ok[k]) continue;
          const double dx = P[k].X() - xh, dy = P[k].Y() - yh,
                       dz = P[k].Z() - zh;
          // "gecen": dugum ucagin KAPLADIGI kutunun icinde (uzerine serilmis)
          //  kutu: govde +-0.50 m, kanat acikligi +-0.90 m, dikey +-0.20 m
          if (std::fabs(dx) < 0.50 && std::fabs(dy) < 0.90 &&
              std::fabs(dz) < 0.20) ++nGecen;
          // "sarma": PERVANE duzlemini (burundan 0.47 m geride) asmis
          //  -> ag ucagin arkasina, pervaneye dogru suruklenmis
          if (dx < -0.40 && std::fabs(dy) < 0.90) ++nSarma;
        }
        // --- PERVANE DISKINDEN GECEN IPLIK SAYISI
        const double xp = xh + this->pervX;
        for (size_t q = 0; q < this->elemanlar.size(); ++q)
        {
          const auto &el = this->elemanlar[q];
          if ((size_t)el.i >= N || (size_t)el.j >= N) continue;
          if (!ok[el.i] || !ok[el.j]) continue;
          const double a1 = P[el.i].X() - xp, a2 = P[el.j].X() - xp;
          if (a1 * a2 > 0.0) continue;              // duzlemi kesmiyor
          const double w = (std::fabs(a1 - a2) < 1e-12) ? 0.0
                           : a1 / (a1 - a2);
          const double yy = P[el.i].Y() + w * (P[el.j].Y() - P[el.i].Y());
          const double zz = P[el.i].Z() + w * (P[el.j].Z() - P[el.i].Z());
          if (std::hypot(yy - yh, zz - zh) < this->pervR)
          {
            ++nPerv;
            if (this->pervGordu.size() < this->elemanlar.size())
              this->pervGordu.assign(this->elemanlar.size(), false);
            if (!this->pervGordu[q])
            { this->pervGordu[q] = true; ++this->nPervToplam; }
          }
        }
      }
      if (n)
        this->log << t - this->firlatmaT + this->devirT << "," << sR / n << "," << sX / n << ","
                  << (nc ? sXc / nc : 0.0) << ","
                  << std::sqrt(std::max(sR2 / n - (sR / n) * (sR / n), 0.0)) << ","
                  << this->Tmax << "," << sV / n << ","
                  << this->Fmax << "," << this->nKirpma << ","
                  << hdx << "," << hv << "," << nGecen << "," << nSarma << ","
                  << this->nKopan << "," << this->n50max << ","
                  << this->n75max << "," << this->n100max << ","
                  << nPerv << "," << this->nPervToplam << "\n";
      this->Tmax = 0.0; this->Fmax = 0.0;
    }

    // ---------- anlik goruntu (3B cizim icin) ----------
    if (this->pozLog.is_open() && t >= this->sonPoz + this->pozDt)
    {
      this->sonPoz = t;
      this->pozLog << (t - this->firlatmaT + this->devirT);
      for (size_t k = 0; k < N; ++k)
        this->pozLog << " " << (ok[k] ? P[k].X() : 0.0)
                     << " " << (ok[k] ? P[k].Y() : 0.0)
                     << " " << (ok[k] ? P[k].Z() : 0.0);
      if (this->hedef != kNullEntity)
      {
        auto hp = Link(this->hedef).WorldPose(_ecm);
        if (hp) this->pozLog << " # hedef " << hp->Pos().X() << " "
                             << hp->Pos().Y() << " " << hp->Pos().Z();
      }
      this->pozLog << "\n";
    }
  }

private:
  /// Tetik konusundan mesaj geldiginde cagrilir (transport is parcacigi).
  void TetikGeldi(const msgs::Boolean &_m)
  {
    if (_m.data() && !this->tetikIstendi.exchange(true))
      gzmsg << "[AgFizik] DISARIDAN TETIK alindi\n";
  }

  /// Atis oncesi: ag dugumlerini firlaticiya gore KINEMATIK tasir.
  /// Dugumler serbest <model>'ler oldugu icin kendiliginden takip etmezler.
  void AgiTasi(EntityComponentManager &_ecm)
  {
    auto fp = Link(this->firlatici).WorldPose(_ecm);
    if (!fp) return;
    if (!this->baslangicAlindi)
    {
      // ilk adimda dugumlerin firlaticiya GORE konumlarini kaydet
      this->baslangicAlindi = true;
      this->yerel.assign(this->dugumlar.size(), math::Pose3d::Zero);
      // Dugum pozlari SDF'te MUTLAK yazili ve URETIM anindaki firlatici
      // pozunu varsayiyorlar. Yerel ofseti O POZA gore hesaplarsak,
      // asagidaki (*fp) * yerel[k] agi firlaticinin GERCEK pozuna tasir
      // -- yani firlatici dunyada nerede olursa olsun ag dogru yerden cikar.
      const math::Pose3d ref = this->uretimPozVar ? this->uretimPoz : *fp;
      for (size_t k = 0; k < this->dugumlar.size(); ++k)
      {
        if (this->dugumlar[k] == kNullEntity) continue;
        auto p = Link(this->dugumlar[k]).WorldPose(_ecm);
        if (p) this->yerel[k] = ref.Inverse() * (*p);
      }
      if (this->uretimPozVar && (this->uretimPoz.Pos() - fp->Pos()).Length() > 1e-3)
        gzmsg << "[AgFizik] ag, firlaticinin GERCEK pozuna tasiniyor "
              << "(uretim " << this->uretimPoz.Pos()
              << " -> gercek " << fp->Pos() << ")\n";
      // ilk adimda da tasimayi uygula (return etme)
    }
    for (size_t k = 0; k < this->dugumlar.size(); ++k)
    {
      if (this->dugumlar[k] == kNullEntity) continue;
      const math::Pose3d hedefPoz = (*fp) * this->yerel[k];
      auto *c = _ecm.Component<components::WorldPoseCmd>(this->dugumlar[k]);
      if (c) c->Data() = hedefPoz;
      else _ecm.CreateComponent(this->dugumlar[k],
                                components::WorldPoseCmd(hedefPoz));
    }
  }

  void HedefTrim(EntityComponentManager &_ecm)
  {
    if (this->hedef == kNullEntity || this->hedefM <= 0.0) return;
    Link(this->hedef).AddWorldForce(
      _ecm, math::Vector3d(0, 0, this->hedefM * 9.81));
  }

  math::Vector3d OrtaKonum(EntityComponentManager &_ecm)
  {
    math::Vector3d s = math::Vector3d::Zero; int n = 0;
    for (auto e : this->dugumlar)
    {
      if (e == kNullEntity) continue;
      auto p = Link(e).WorldPose(_ecm);
      if (p) { s += p->Pos(); ++n; }
    }
    return n ? s / n : math::Vector3d::Zero;
  }

  Entity dunya{kNullEntity};
  std::vector<Entity> dugumlar, bilyeler;
  std::vector<Eleman> elemanlar;
  double EA{100.0}, zeta{0.30}, dIplik{1.65e-4}, Cdn{1.10}, Cdt{0.03};
  double aeroOlcek{1.0}, rho{1.225}, bilyeCd{0.47}, bilyeD{0.0127};
  double firlatmaT{0.0}, vEks{34.5}, vRad{8.0}, Rref{0.02};
  double mDugum{2.76e-5}, Fsinir{200.0}, Fmax{0.0}, Tkopma{64.15}, Tzirve{0.0};
  long nKirpma{0}, nKopan{0};
  double Tdugum{35.3};
  int n50max{0}, n75max{0}, n100max{0};
  double pervX{-0.47}, pervR{0.115};
  std::vector<bool> pervGordu;
  long nPervToplam{0};
  bool iraksadi{false};
  Entity hedef{kNullEntity}, firlatici{kNullEntity};
  std::string tetikKonu, firlaticiAd;
  math::Pose3d firlaticiP0, uretimPoz;
  bool uretimPozVar{false};
  std::vector<math::Pose3d> yerel;
  bool baslangicAlindi{false};
  std::atomic<bool> tetikIstendi{false};
  transport::Node dugum;
  std::string hedefAd;
  std::map<int, math::Vector3d> devirHiz;
  double devirT{0.0};
  math::Vector3d hedefP0{math::Vector3d::Zero};
  double hedefM{0.0};
  math::Vector3d ruzgar{math::Vector3d::Zero};
  std::vector<int> bilyeIdx;
  std::string dugumOn{"dugum_"}, bilyeOn{"bilye_"};
  bool kesfedildi{false}, cmdTemizlendi{false};
  std::string logYol;
  std::ofstream log, pozLog;
  std::string pozYol;
  double pozDt{0.01}, sonPoz{-1e9};
  double logDt{0.005}, sonLog{-1e9}, Tmax{0.0};
  bool atildi{false};
};
}  // namespace ag

GZ_ADD_PLUGIN(ag::AgFizik, gz::sim::System,
              ag::AgFizik::ISystemConfigure,
              ag::AgFizik::ISystemPreUpdate)
GZ_ADD_PLUGIN_ALIAS(ag::AgFizik, "ag::AgFizik")
