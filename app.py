from flask import Flask, render_template, request
import pandas as pd
import numpy as np 

app = Flask(__name__)

# Load the transportation dataset
df = pd.read_csv("multimodal_mobility_network.csv")

print("Dataset loaded:", df.shape)

# Build the transportation network
connections = df[
    ["connection_id", "source", "destination"]
].drop_duplicates()

network = {}

for index, row in connections.iterrows():
    source = row["source"]
    destination = row["destination"]

    if source not in network:
        network[source] = set()

    if destination not in network:
        network[destination] = set()

    network[source].add(destination)
    network[destination].add(source)

for location in network:
    network[location] = list(network[location])

print("Network locations:", len(network))
print("Network connections:", len(connections))

# Find possible paths between two locations
def find_paths(network, source, destination):
    paths = []

    def search(current, path):
        if current == destination:
            paths.append(path.copy())
            return

        for next_location in network[current]:
            if next_location not in path:
                path.append(next_location)
                search(next_location, path)
                path.pop()

    search(source, [source])

    return paths

# Get individual segments from a path
def get_segments(path):
    segments = []

    for i in range(len(path) - 1):
        segments.append((path[i], path[i + 1]))

    return segments

# Get transportation options for each segment
def get_segment_options(path, df):
    segment_options = []

    segments = get_segments(path)

    for source, destination in segments:
        options = df[
            (
                (df["source"] == source) &
                (df["destination"] == destination)
            )
            |
            (
                (df["source"] == destination) &
                (df["destination"] == source)
            )
        ].copy()

        segment_options.append(options)

    return segment_options

# Filter transportation options based on user-selected modes
def get_available_modes(segment_options, available_modes):
    mode_options = []

    for options in segment_options:
        modes_for_segment = options[
            options["mode"].isin(available_modes)
        ].copy()

        mode_options.append(modes_for_segment)

    return mode_options

# Generate multimodal journeys for a path
def generate_multimodal_journeys(
    path,
    mode_options,
    max_time,
    max_budget
):
    journeys = [
        {
            "modes": [],
            "total_time": 0,
            "total_cost": 0,
            "total_co2": 0
        }
    ]

    for options in mode_options:

        new_journeys = []

        for journey in journeys:

            for _, row in options.iterrows():

                new_time = (
                    journey["total_time"]
                    + row["duration_min"]
                )

                new_cost = (
                    journey["total_cost"]
                    + row["cost_inr"]
                )

                # Check time constraint
                if exceeds_time_limit(
                    new_time,
                    max_time
                ):
                    continue

                # Check budget constraint
                if exceeds_budget_limit(
                    new_cost,
                    max_budget
                ):
                    continue

                new_journey = {
                    "modes": journey["modes"] + [row["mode"]],
                    "total_time": new_time,
                    "total_cost": new_cost,
                    "total_co2": (
                        journey["total_co2"]
                        + row["co2_kg"]
                    )
                }

                new_journeys.append(new_journey)

        # Remove dominated journeys BEFORE
        # continuing to the next segment
        journeys = prune_dominated_journeys(
            new_journeys
        )

        if not journeys:
            break

    results = []

    for journey in journeys:

        results.append({
            "path": path,
            "modes": journey["modes"],
            "total_time": journey["total_time"],
            "total_cost": journey["total_cost"],
            "total_co2": journey["total_co2"]
        })

    return pd.DataFrame(results)

# Check whether a journey exceeds the time limit
def exceeds_time_limit(current_time, max_time):
    return current_time > max_time


# Check whether a journey exceeds the budget limit
def exceeds_budget_limit(current_cost, max_budget):
    return current_cost > max_budget

# Check whether a path can satisfy the user's constraints
def is_path_feasible(
    path,
    df,
    available_modes,
    max_time,
    max_budget
):
    total_min_time = 0
    total_min_cost = 0

    for i in range(len(path) - 1):
        source = path[i]
        destination = path[i + 1]

        options = df[
            (
                (df["source"] == source) &
                (df["destination"] == destination)
            )
            |
            (
                (df["source"] == destination) &
                (df["destination"] == source)
            )
        ]

        options = options[
            options["mode"].isin(available_modes)
        ]

        if options.empty:
            return False

        total_min_time += options["duration_min"].min()
        total_min_cost += options["cost_inr"].min()

    return (
        total_min_time <= max_time
        and
        total_min_cost <= max_budget
    )

# Keep only paths that satisfy the user's constraints
def process_feasible_paths(
    paths,
    df,
    available_modes,
    max_time,
    max_budget
):
    feasible_paths = []

    for path in paths:
        if is_path_feasible(
            path,
            df,
            available_modes,
            max_time,
            max_budget
        ):
            feasible_paths.append(path)

    return feasible_paths

# Generate all feasible multimodal journeys
def generate_feasible_journeys(
    feasible_paths,
    df,
    available_modes,
    max_time,
    max_budget
):
    all_journeys = []

    for path in feasible_paths:

        segment_options = get_segment_options(
            path,
            df
        )

        mode_options = get_available_modes(
            segment_options,
            available_modes
        )

        path_journeys = generate_multimodal_journeys(
            path,
            mode_options,
            max_time,
            max_budget
        )

        if not path_journeys.empty:
            all_journeys.append(path_journeys)

    if not all_journeys:
        return pd.DataFrame(
            columns=[
                "path",
                "modes",
                "total_time",
                "total_cost",
                "total_co2"
            ]
        )

    return pd.concat(
        all_journeys,
        ignore_index=True
    )

# Generate alternative routes when no feasible route exists
def generate_alternative_routes(
    source,
    destination,
    df,
    available_modes
):
    paths = find_paths(
        network,
        source,
        destination
    )

    alternative_journeys = []

    for path in paths:

        segment_options = get_segment_options(
            path,
            df
        )

        mode_options = get_available_modes(
            segment_options,
            available_modes
        )

        # Skip paths where a segment has no selected mode
        if any(
            options.empty
            for options in mode_options
        ):
            continue

        # Select the best option for each segment
        selected_modes = []
        total_time = 0
        total_cost = 0
        total_co2 = 0

        for options in mode_options:

            best_option = (
                options
                .sort_values(
                    ["duration_min", "cost_inr", "co2_kg"]
                )
                .iloc[0]
            )

            selected_modes.append(
                best_option["mode"]
            )

            total_time += best_option["duration_min"]
            total_cost += best_option["cost_inr"]
            total_co2 += best_option["co2_kg"]

        alternative_journeys.append({
            "path": path,
            "modes": selected_modes,
            "total_time": total_time,
            "total_cost": total_cost,
            "total_co2": total_co2
        })

    if not alternative_journeys:
        return pd.DataFrame(
            columns=[
                "path",
                "modes",
                "total_time",
                "total_cost",
                "total_co2"
            ]
        )

    return pd.DataFrame(
        alternative_journeys
    )

# Select the closest alternatives to the user's constraints
def get_closest_alternatives(
    alternative_routes,
    max_time,
    max_budget,
    number_of_routes=3
):
    alternatives = alternative_routes.copy()

    if alternatives.empty:
        return alternatives

    alternatives["extra_time"] = (
        alternatives["total_time"] - max_time
    ).clip(lower=0)

    alternatives["extra_budget"] = (
        alternatives["total_cost"] - max_budget
    ).clip(lower=0)

    alternatives["alternative_score"] = (
        alternatives["extra_time"].rank(pct=True)
        + alternatives["extra_budget"].rank(pct=True)
        + alternatives["total_co2"].rank(pct=True)
    )

    return (
        alternatives
        .sort_values("alternative_score")
        .head(number_of_routes)
        .drop(columns="alternative_score")
        .reset_index(drop=True)
    )
    

# Check whether one journey is dominated by another
def is_dominated(journey, other_journey):
    return (
        other_journey["total_time"] <= journey["total_time"]
        and
        other_journey["total_cost"] <= journey["total_cost"]
        and
        other_journey["total_co2"] <= journey["total_co2"]
        and
        (
            other_journey["total_time"] < journey["total_time"]
            or
            other_journey["total_cost"] < journey["total_cost"]
            or
            other_journey["total_co2"] < journey["total_co2"]
        )
    )

# Remove dominated partial journeys during generation
def prune_dominated_journeys(journeys):

    non_dominated = []

    for journey in journeys:

        dominated = False

        for other_journey in journeys:

            if journey is other_journey:
                continue

            if is_dominated(
                journey,
                other_journey
            ):
                dominated = True
                break

        if not dominated:
            non_dominated.append(journey)

    return non_dominated


# Remove dominated journeys
def remove_dominated_routes(journeys):
    non_dominated = []

    for _, journey in journeys.iterrows():
        dominated = False

        for _, other_journey in journeys.iterrows():

            if is_dominated(
                journey,
                other_journey
            ):
                dominated = True
                break

        if not dominated:
            non_dominated.append(journey)

    if not non_dominated:
        return pd.DataFrame(
            columns=[
                "path",
                "modes",
                "total_time",
                "total_cost",
                "total_co2"
            ]
        )

    return pd.DataFrame(
        non_dominated
    ).reset_index(drop=True)

# Select up to 3 route options
def select_top_routes(journeys):
    if journeys.empty:
        return journeys.copy()

    candidate_routes = journeys.copy()

    candidate_routes["route_score"] = (
        candidate_routes["total_time"].rank(pct=True)
        + candidate_routes["total_cost"].rank(pct=True)
        + candidate_routes["total_co2"].rank(pct=True)
    )

    top_routes = (
        candidate_routes
        .sort_values("route_score")
        .head(3)
        .drop(columns="route_score")
        .reset_index(drop=True)
    )

    return top_routes

# Calculate a balanced recommendation score
def calculate_recommendation_score(routes):
    routes = routes.copy()

    routes["recommendation_score"] = (
        routes["total_time"].rank(pct=True)
        + routes["total_cost"].rank(pct=True)
        + routes["total_co2"].rank(pct=True)
    )

    return routes

# Select the recommended route
def recommend_route(routes):

    if routes.empty:
        return routes.copy()

    recommended_route = (
        routes
        .sort_values("recommendation_score")
        .head(1)
        .reset_index(drop=True)
    )

    recommended_route["recommendation_reason"] = (
        "This route was recommended because it provides "
        "a balanced combination of travel time, cost, and CO2 emissions "
        "among the available feasible routes."
    )

    return recommended_route

# Main route planning function for user inputs
def plan_routes(
    source,
    destination,
    max_budget,
    max_time,
    available_modes
):
    paths = find_paths(
        network,
        source,
        destination
    )

    feasible_paths = process_feasible_paths(
        paths,
        df,
        available_modes,
        max_time,
        max_budget
    )

    feasible_journeys = generate_feasible_journeys(
        feasible_paths,
        df,
        available_modes,
        max_time,
        max_budget
    )

    # If feasible routes exist
    if not feasible_journeys.empty:

        non_dominated_journeys = remove_dominated_routes(
            feasible_journeys
        )

        top_routes = select_top_routes(
            non_dominated_journeys
        )

        scored_routes = calculate_recommendation_score(
            top_routes
        )

        recommended_route = recommend_route(
            scored_routes
        )

        return {
            "status": "feasible",
            "paths": paths,
            "feasible_paths": feasible_paths,
            "feasible_journeys": feasible_journeys,
            "routes": scored_routes,
            "recommended_route": recommended_route,
            "alternative_routes": pd.DataFrame()
        }

    # If no feasible routes exist
    alternative_routes = generate_alternative_routes(
        source,
        destination,
        df,
        available_modes
    )

    closest_alternatives = get_closest_alternatives(
        alternative_routes,
        max_time,
        max_budget
    )

    return {
        "status": "no_feasible_route",
        "paths": paths,
        "feasible_paths": feasible_paths,
        "feasible_journeys": feasible_journeys,
        "routes": pd.DataFrame(),
        "recommended_route": pd.DataFrame(),
        "alternative_routes": closest_alternatives
    }


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        source = request.form["source"]
        destination = request.form["destination"]

        max_budget = float(
            request.form["max_budget"]
        )

        max_time = float(
            request.form["max_time"]
        )

        available_modes = request.form.getlist("modes")

        result = plan_routes(
            source,
            destination,
            max_budget,
            max_time,
            available_modes
        )

        return render_template(
            "index.html",
            locations=sorted(network.keys()),
            result=result
        )

    return render_template(
        "index.html",
        locations=sorted(network.keys())
    )



if __name__ == "__main__":
    app.run(debug=True)