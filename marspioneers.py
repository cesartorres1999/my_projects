"""
Mars Sustainable Settlement Simulator
-------------------------------------
No external libraries, no randomness.
Every subsystem is a function with a mission-linked docstring.
Inputs gathered via input(); outputs formatted with f-strings.
"""

# ---------- Subsystems ----------

def mission_brief(crew_size: int) -> dict:
    """
    Mission Brief (Orchestration Context)
    -------------------------------------
    Role: Frame the mission objectives and constraints for a sustainable human
    settlement on Mars. Converts crew size into core survival targets that
    downstream subsystems will satisfy (O2, water, energy, food, mobility, comms).
    Returns a dict baseline all subsystems can read.
    """
    brief = {
        "crew": crew_size,
        # Assumptions (simple, instructional model):
        # Oxygen: 550 L O2 / person / day
        # Water: 15 L / person / day (drinking, hygiene, cooking) before recycling
        # Food: 3 kg / person / day (fresh mass equivalent)
        "o2_need_L_per_day": 550 * crew_size,
        "water_need_L_per_day": 15 * crew_size,
        "food_need_kg_per_day": 3 * crew_size
    }
    print(f"Mission Brief: Establishing survival base for {crew_size} crew members.")
    print(f"Targets -> O2: {brief['o2_need_L_per_day']:.2f} L/day, "
          f"Water: {brief['water_need_L_per_day']:.2f} L/day, "
          f"Food: {brief['food_need_kg_per_day']:.2f} kg/day.")
    return brief


def energy_system(solar_kwh: float, battery_kwh: float, crew: int) -> dict:
    """
    Energy System
    -------------
    Role: Convert total available daily energy (solar + battery discharge allowance)
    into prioritized allocations that keep life-critical loops alive.
    Priority order: Life Support > Water > Food > Comms > Transport.
    Returns allocation dict and any shortfall.
    """
    total_kwh = solar_kwh + battery_kwh

    # Minimal daily budgets to keep each loop 'alive' (teaching values):
    min_life_support = max(10.0, 5.0 + 1.5 * crew)  # scales with crew
    min_water = 12.0                                 # recycling pumps, purification
    min_food = 25.0                                  # lights, pumps, control
    min_comms = 6.0                                   # baseband + relay
    min_transport = 0.0                               # optional unless operations day

    required_min = min_life_support + min_water + min_food + min_comms + min_transport

    allocations = {"life_support": 0.0, "water": 0.0, "food": 0.0, "comms": 0.0, "transport": 0.0}
    shortfall = 0.0
    remaining = total_kwh

    def allocate(name, need):
        nonlocal remaining
        give = min(need, remaining)
        allocations[name] = give
        remaining -= give

    # Allocate by priority
    allocate("life_support", min_life_support)
    allocate("water", min_water)
    allocate("food", min_food)
    allocate("comms", min_comms)
    allocate("transport", min_transport)

    if total_kwh < required_min:
        shortfall = required_min - total_kwh

    print(f"Energy System: {total_kwh:.2f} kWh available "
          f"(Solar: {solar_kwh:.2f}, Battery: {battery_kwh:.2f}).")
    for k, v in allocations.items():
        print(f"  • {k.capitalize()} allocation: {v:.2f} kWh")
    if shortfall > 0:
        print(f"  !! Energy shortfall: {shortfall:.2f} kWh vs. minimal daily need {required_min:.2f} kWh")
    else:
        print("  Energy status: Minimal priorities met.")
    return {"total_kwh": total_kwh, "allocations": allocations, "shortfall": shortfall}


def life_support(crew: int, energy_kwh: float) -> dict:
    """
    Life Support (Oxygen Loop)
    --------------------------
    Role: Meet breathable oxygen demand via electrolysis & bioregenerative assist.
    Model: oxygen production scales with allocated energy (instructional constant).
    Assumptions:
      - O2 need = 550 L/person/day.
      - Production rate = 300 L O2 per kWh allocated (simplified).
      - Electrolysis water use ~ 0.45 L per 300 L O2 (teaching placeholder).
    Returns O2 production, deficit, and water consumed by electrolysis.
    """
    need_L = 550 * crew
    produced_L = 300.0 * energy_kwh
    water_for_o2_L = (produced_L / 300.0) * 0.45  # ~0.45 L per 300 L O2
    deficit_L = max(0.0, need_L - produced_L)

    print(f"Life Support: O2 need {need_L:.2f} L; production {produced_L:.2f} L "
          f"using {energy_kwh:.2f} kWh; deficit {deficit_L:.2f} L.")
    return {
        "o2_need_L": need_L,
        "o2_produced_L": produced_L,
        "o2_deficit_L": deficit_L,
        "water_for_o2_L": water_for_o2_L
    }


def water_system(crew: int, water_reserve_L: float, energy_kwh: float, hydroponics_withdrawal_L: float) -> dict:
    """
    Water Management
    ----------------
    Role: Balance potable & process water with closed-loop recycling.
    Model:
      - Base demand = 15 L/person/day.
      - Hydroponics withdrawal is provided by Food subsystem.
      - Recycling recovers 80% of all non-consumptive use (teaching constant).
      - Energy powers pumps & purification; if < 8 kWh, recycling drops to 60%.
    Returns closing reserve, net balance, and effective recycling rate.
    """
    base_demand = 15.0 * crew
    total_withdrawal = base_demand + hydroponics_withdrawal_L

    recycle_rate = 0.8 if energy_kwh >= 8.0 else 0.6
    recovered = total_withdrawal * recycle_rate
    net_use = total_withdrawal - recovered

    closing_reserve = water_reserve_L - net_use
    status = "stable" if closing_reserve >= 0 else "depleting"

    print(f"Water System: Demand {total_withdrawal:.2f} L "
          f"(crew {base_demand:.2f} + hydro {hydroponics_withdrawal_L:.2f}); "
          f"recycling {recycle_rate*100:.0f}% -> recovered {recovered:.2f} L; "
          f"net use {net_use:.2f} L; reserve -> {closing_reserve:.2f} L ({status}).")
    return {
        "recycle_rate": recycle_rate,
        "base_demand_L": base_demand,
        "hydro_withdraw_L": hydroponics_withdrawal_L,
        "recovered_L": recovered,
        "net_use_L": net_use,
        "closing_reserve_L": closing_reserve,
        "status": status
    }


def food_system(crew: int, area_m2: float, energy_kwh: float, water_available_L: float) -> dict:
    """
    Food Production (Hydroponics)
    -----------------------------
    Role: Produce fresh edible biomass to meet daily caloric mass target.
    Model (instructional):
      - Need = 3.0 kg/person/day.
      - Yield = 0.04 kg/m²/day base + 0.02 kg per kWh allocated (capped by water).
      - Hydroponics water withdrawal = 2.0 L per kg produced (teaching constant).
    Returns production, deficit, and the water requested from Water System.
    """
    need_kg = 3.0 * crew
    potential_from_area = 0.04 * area_m2
    potential_from_energy = 0.02 * energy_kwh
    raw_production = potential_from_area + potential_from_energy

    water_needed = max(0.0, raw_production * 2.0)
    # Cap production by water availability (if limited upstream reserve)
    if water_needed > water_available_L:
        # scale down proportionally
        scale = water_available_L / water_needed if water_needed > 0 else 0.0
        production_kg = raw_production * scale
        water_draw_L = water_available_L
    else:
        production_kg = raw_production
        water_draw_L = water_needed

    deficit_kg = max(0.0, need_kg - production_kg)

    print(f"Food System: Need {need_kg:.2f} kg; production {production_kg:.2f} kg "
          f"(area {potential_from_area:.2f} + energy {potential_from_energy:.2f}); "
          f"water draw {water_draw_L:.2f} L; deficit {deficit_kg:.2f} kg.")
    return {
        "food_need_kg": need_kg,
        "food_produced_kg": production_kg,
        "food_deficit_kg": deficit_kg,
        "hydroponics_water_draw_L": water_draw_L
    }


def comms_system(required_uptime_h: float, energy_kwh: float) -> dict:
    """
    Communications
    --------------
    Role: Maintain continuous communication windows (orbiter relay + baseband).
    Model:
      - Energy need = 0.5 kWh per hour uptime.
      - If allocation < need, uptime is reduced proportionally.
    Returns achieved uptime and any shortfall.
    """
    need_kwh = 0.5 * required_uptime_h
    if need_kwh <= 0:
        achieved_h = 0.0
        shortfall_h = 0.0
    else:
        ratio = min(1.0, energy_kwh / need_kwh)
        achieved_h = required_uptime_h * ratio
        shortfall_h = required_uptime_h - achieved_h

    print(f"Comms: Required {required_uptime_h:.2f} h; achieved {achieved_h:.2f} h "
          f"with {energy_kwh:.2f} kWh; shortfall {shortfall_h:.2f} h.")
    return {"required_h": required_uptime_h, "achieved_h": achieved_h, "shortfall_h": shortfall_h}


def transport_system(num_rovers: int, energy_kwh: float) -> dict:
    """
    Surface Transport
    -----------------
    Role: Provide rover mobility for EVA logistics & sampling.
    Model:
      - Baseline readiness if num_rovers >= 1.
      - Range = 50 km per rover baseline + (2.0 km per kWh allocated).
    Returns deployed rover count and total operational range.
    """
    deployed = max(0, num_rovers)
    range_km = deployed * 50.0 + 2.0 * energy_kwh
    print(f"Transport: {deployed} rover(s) ready; operational range {range_km:.2f} km "
          f"given {energy_kwh:.2f} kWh.")
    return {"rovers": deployed, "range_km": range_km}


# ---------- Orchestrator & Flow Map ----------

def flow_map():
    """
    Prints an ASCII data/resource flow map to illustrate subsystem interactions.
    """
    print("\nResource/Data Flow Map")
    print("----------------------")
    print("   Solar/Battery --> ENERGY SYS --> {allocations to: Life, Water, Food, Comms, Transport}")
    print("           ENERGY --> LIFE SUPPORT --> uses water (electrolysis) --> O2 to Habitat")
    print("           ENERGY --> WATER SYS <---- hydroponics water draw request from FOOD")
    print("           ENERGY --> FOOD SYS  ----> biomass (food) to Habitat; water draw to WATER")
    print("           ENERGY --> COMMS ----> achieved uptime (ops data link)")
    print("           ENERGY --> TRANSPORT ----> rover range (km)")
    print("   HABITAT (crew demand): O2, Water, Food consumed; feedback -> next-day planning\n")


def simulate():
    # ---- Gather Inputs (no hard-coded mission values) ----
    crew = int(input("Enter crew size: ").strip())
    solar = float(input("Enter available solar energy (kWh): ").strip())
    battery = float(input("Enter available battery energy for the day (kWh): ").strip())
    water_reserve = float(input("Enter current water reserve (L): ").strip())
    greenhouse_area = float(input("Enter greenhouse growing area (m^2): ").strip())
    rovers = int(input("Enter number of available rovers: ").strip())
    comms_uptime_req = float(input("Enter required communications uptime (hours): ").strip())

    # ---- Mission Brief ----
    brief = mission_brief(crew)

    # ---- Energy Allocation ----
    power = energy_system(solar, battery, crew)

    # ---- Life Support (O2) ----
    o2 = life_support(crew, power["allocations"]["life_support"])

    # ---- Food Production (requests water, consumes energy) ----
    # For coupling, pass a *provisional* water availability (current reserve),
    # Water system will enforce actual reserve later.
    food = food_system(
        crew=crew,
        area_m2=greenhouse_area,
        energy_kwh=power["allocations"]["food"],
        water_available_L=water_reserve
    )

    # ---- Water System (closes the loop with actual reserve & food water draw) ----
    water = water_system(
        crew=crew,
        water_reserve_L=water_reserve - o2["water_for_o2_L"],  # electrolysis draw first
        energy_kwh=power["allocations"]["water"],
        hydroponics_withdrawal_L=food["hydroponics_water_draw_L"]
    )

    # ---- Communications ----
    comms = comms_system(comms_uptime_req, power["allocations"]["comms"])

    # ---- Transport ----
    transport = transport_system(rovers, power["allocations"]["transport"])

    # ---- Flow Map ----
    flow_map()

    # ---- Summary across essential resources ----
    print("Essential Resources Summary")
    print("---------------------------")
    print(f"OXYGEN -> need {o2['o2_need_L']:.2f} L, produced {o2['o2_produced_L']:.2f} L, "
          f"deficit {o2['o2_deficit_L']:.2f} L, water used {o2['water_for_o2_L']:.2f} L.")
    print(f"WATER  -> opening {water_reserve:.2f} L, net use {water['net_use_L']:.2f} L, "
          f"closing {water['closing_reserve_L']:.2f} L (status: {water['status']}).")
    print(f"ENERGY -> total {power['total_kwh']:.2f} kWh, shortfall {power['shortfall']:.2f} kWh.")
    print(f"FOOD   -> need {food['food_need_kg']:.2f} kg, produced {food['food_produced_kg']:.2f} kg, "
          f"deficit {food['food_deficit_kg']:.2f} kg.")
    print(f"COMMS  -> required {comms['required_h']:.2f} h, achieved {comms['achieved_h']:.2f} h, "
          f"shortfall {comms['shortfall_h']:.2f} h.")
    print(f"TRANSPORT -> rovers {transport['rovers']}, range {transport['range_km']:.2f} km.")

    # ---- Mission completion verdict ----
    critical_ok = (o2["o2_deficit_L"] == 0.0) and (water["status"] == "stable") and (food["food_deficit_kg"] == 0.0)
    if critical_ok and power["shortfall"] == 0.0:
        verdict = "All systems stable."
    elif critical_ok:
        verdict = "Critical life-support stable; optimize energy and operations."
    else:
        verdict = "Critical deficits present – reallocate or reduce load."

    print(f"\nSimulation complete: {verdict}")


# Run once when the script is executed directly
if __name__ == "__main__":
    simulate()

# 1) Normal scenario (balanced)
# Enter crew size: 4
# Enter available solar energy (kWh): 200
# Enter available battery energy for the day (kWh): 20
# Enter current water reserve (L): 1200
# Enter greenhouse growing area (m^2): 180
# Enter number of available rovers: 1
# Enter required communications uptime (hours): 12

# 2) Edge scenario (uncrewed maintenance day)
# Enter crew size: 0
# Enter available solar energy (kWh): 60
# Enter available battery energy for the day (kWh): 0
# Enter current water reserve (L): 500
# Enter greenhouse growing area (m^2): 50
# Enter number of available rovers: 0
# Enter required communications uptime (hours): 6

# 3) Failure scenario (energy-starved with small water reserve)
# Enter crew size: 6
# Enter available solar energy (kWh): 20
# Enter available battery energy for the day (kWh): 0
# Enter current water reserve (L): 150
# Enter greenhouse growing area (m^2): 60
# Enter number of available rovers: 1
# Enter required communications uptime (hours): 16











