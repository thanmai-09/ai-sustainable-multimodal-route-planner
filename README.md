# AI-Powered Sustainable Multimodal Route Planner

A route planning and recommendation system that evaluates multimodal journeys based on travel time, cost, transportation availability, and CO₂ emissions.

Users can specify their source, destination, travel constraints, and available transportation modes. The system evaluates connected routes, supports different modes across route segments, and presents feasible alternatives.

---

## Key Features

- Multimodal route planning
- Multiple transportation modes across route segments
- Travel time and budget constraints
- CO₂ emission evaluation
- Route comparison and filtering
- Dominated-route removal
- Top three feasible route options
- Balanced route recommendation
- Recommendation explanation
- No-feasible-route handling
- Closest alternative routes with additional time and budget
- Web-based Flask interface

---

## How It Works

1. The user selects a source and destination.
2. The user specifies a maximum budget and travel time.
3. The user selects the transportation modes available to them.
4. The system identifies connected paths between the selected locations.
5. Available transportation modes are evaluated for each route segment.
6. Routes exceeding the specified time or budget are filtered out.
7. Dominated routes are removed based on travel time, cost, and CO₂ emissions.
8. Up to three feasible route options are selected.
9. A recommendation score is used to identify a balanced route.
10. If no feasible route exists, the system provides alternative routes with their additional time and budget requirements.

---

## Recommendation Approach

Each feasible journey is evaluated using:

- **Travel Time**
- **Cost**
- **CO₂ Emissions**

A route is considered dominated when another route performs no worse across all three metrics and is better in at least one.

After dominated routes are removed, the remaining routes are ranked using a combined score based on their relative travel time, cost, and CO₂ emissions.

The route with the lowest score is presented as the recommended option.

---

## Route Sustainability Comparison

The system provides a comparison of the displayed routes using relative percentages for:

- **Time Efficiency** – compares each route's travel time with the fastest displayed route.
- **Cost Efficiency** – compares each route's cost with the cheapest displayed route.
- **CO₂ Efficiency** – compares each route's emissions with the lowest-emission displayed route.

This allows users to understand the trade-offs between travel time, cost, and environmental impact across the available routes.

---

## No-Feasible-Route Handling

When no route satisfies both the user's time and budget constraints, the system does not present an infeasible route as a valid option.

Instead, it provides alternative routes with:

- Actual travel time
- Actual cost
- CO₂ emissions
- Additional time required
- Additional budget required

---

## Dataset

The project uses a synthetic multimodal mobility dataset containing estimated transportation information for a predefined network of connected urban locations.

The dataset includes:

- Connection ID
- Source
- Destination
- Transportation mode
- Distance
- Duration
- Cost
- CO₂ emissions

The prototype does not depend on external map services, live transportation APIs, or paid APIs.

---

## Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **Flask**
- **HTML**
- **CSS**
- **Jupyter Notebook**
- **Git**

---

## Project Structure

```text
ai-sustainable-multimodal-route-planner/
│
├── app.py
├── README.md
├── requirements.txt
├── multimodal_mobility_network.csv
├── create_sustainable_mobility_dataset.ipynb
├── sustainable_multimodal_route_planner.ipynb
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/thanmai-09/ai-sustainable-multimodal-route-planner.git
cd ai-sustainable-multimodal-route-planner
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Open the local Flask address displayed in the terminal:

```text
http://127.0.0.1:5000/
```

---

## Responsible AI

The project incorporates responsible AI considerations through:

- Transparent route metrics and recommendation criteria
- Clear distinction between feasible and infeasible routes
- Explanation of the recommended route
- Use of synthetic and estimated prototype data
- No unnecessary collection of personal or sensitive information
- User visibility into the factors considered during route selection

---

## Limitations

- Transportation values are synthetic or estimated for prototype purposes.
- No live traffic information is used.
- No live public transportation data is used.
- No live GPS navigation is provided.
- Booking and payment are not supported.
- CO₂ values are estimated for prototype evaluation.
- The current system operates on a predefined transportation network.

---

## Future Enhancements

- Real-time transportation and traffic data
- Map-based route visualization
- User-defined optimization priorities for time, cost, or CO₂
- More detailed carbon-emission estimation
- Larger and dynamically generated transportation networks
- Support for additional cities
- Real-time route updates
