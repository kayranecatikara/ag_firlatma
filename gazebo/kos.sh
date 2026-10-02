#!/usr/bin/env bash
# Ag firlatma Gazebo kosulari.
#
#   ./gazebo/kos.sh dogrulama        carpisma YOK, hizli, Python ile karsilastirma
#   ./gazebo/kos.sh yakalama [gui]   hedef + temas (zamanli atis)
#   ./gazebo/kos.sh entegrasyon [gui]
#        MONTE EDILEBILIR model paketi + HARICI TETIK.
#        Baska bir araca entegrasyonu denemek icin. Atis icin:
#          gz topic -t /ag_firlatici/ates -m gz.msgs.Boolean -p "data: true"
#        Bkz. README "Baska bir araca entegrasyon".
set -e
KOK="$(cd "$(dirname "$0")/.." && pwd)"
MOD="${1:-dogrulama}"
SURE="${AG_SURE:-0.75}"

case "$MOD" in
  dogrulama)   export AG_CARPISMA=0 ;;
  yakalama)    export AG_CARPISMA=1 ;;
  entegrasyon) export AG_CARPISMA=1 AG_FIRLATICI=1 AG_TETIK=harici
               export AG_ORGU="${AG_ORGU:-kare}" AG_RAG="${AG_RAG:-1.3}" AG_GOZ="${AG_GOZ:-0.20}"
               export GZ_SIM_RESOURCE_PATH="$KOK/gazebo/models:${GZ_SIM_RESOURCE_PATH:-}"
               python3 "$KOK/gazebo/scripts/model_paketi_uret.py" >/dev/null ;;
  *) echo "bilinmeyen mod: $MOD  (dogrulama | yakalama | entegrasyon)"; exit 1 ;;
esac

export GZ_SIM_SYSTEM_PLUGIN_PATH="$KOK/gazebo/plugin/build"
python3 "$KOK/gazebo/scripts/ag_sdf_uret.py"

DT=$(grep -oP '(?<=<max_step_size>)[0-9.e-]+' "$KOK/gazebo/worlds/ag_atis.sdf")
ADIM=$(python3 -c "print(int($SURE/$DT))")
echo "--- $MOD : dt=$DT s, $ADIM adim ($SURE s sim) ---"
if [ "$MOD" = "entegrasyon" ]; then
  echo "    ATES ETMEK ICIN (baska bir terminalde):"
  echo "    gz topic -t /ag_firlatici/ates -m gz.msgs.Boolean -p \"data: true\""
fi

GUI=""; [ "$2" = "gui" ] || GUI="-s"
gz sim $GUI -r -v 3 --iterations "$ADIM" "$KOK/gazebo/worlds/ag_atis.sdf"
