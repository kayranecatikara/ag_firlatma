#!/usr/bin/env bash
# Ag firlatma Gazebo kosusu.
#   ./gazebo/kos.sh dogrulama   -> carpisma YOK, hizli, Python ile karsilastirma
#   ./gazebo/kos.sh yakalama    -> hedef + temas var
#   ./gazebo/kos.sh yakalama gui-> ustune GUI ac
set -e
KOK="$(cd "$(dirname "$0")/.." && pwd)"
MOD="${1:-dogrulama}"
SURE="${AG_SURE:-0.75}"            # simule edilecek sim-zamani [s]

[ "$MOD" = "dogrulama" ] && export AG_CARPISMA=0 || export AG_CARPISMA=1

export GZ_SIM_SYSTEM_PLUGIN_PATH="$KOK/gazebo/plugin/build"
python3 "$KOK/gazebo/scripts/ag_sdf_uret.py"

DT=$(grep -oP '(?<=<max_step_size>)[0-9.e-]+' "$KOK/gazebo/worlds/ag_atis.sdf")
ADIM=$(python3 -c "print(int($SURE/$DT))")
echo "--- $MOD : dt=$DT s, $ADIM adim ($SURE s sim) ---"

GUI=""; [ "$2" = "gui" ] || GUI="-s"
gz sim $GUI -r -v 3 --iterations "$ADIM" "$KOK/gazebo/worlds/ag_atis.sdf"
