# AI-Powered Sustainable Multimodal Route Planner

An AI-powered prototype for sustainable urban journey planning that evaluates multimodal routes based on travel time, cost, transportation availability, and CO₂ emissions.

The system allows users to combine different transportation modes across different segments of a journey and provides feasible route options based on their time and budget constraints.

The project focuses on sustainable urban mobility and aligns with **SDG 11 – Sustainable Cities and Communities** and **SDG 13 – Climate Action**.

---

## Overview

Urban travelers often need to balance multiple factors when choosing how to travel, including:

- Travel time
- Travel cost
- Available transportation modes
- Environmental impact

This project addresses this challenge through a route planning and recommendation system that evaluates connected transportation paths and multimodal combinations.

Users can specify their source, destination, maximum budget, maximum travel time, and available transportation modes. The system evaluates possible journeys and presents suitable route options.

---

## Key Features

- Multimodal route planning
- Different transportation modes across route segments
- Maximum travel time constraint
- Maximum budget constraint
- CO₂ emission evaluation
- Route comparison
- Dominated-route filtering
- Top three feasible route options
- Balanced route recommendation
- Recommendation explanation
- No-feasible-route handling
- Closest alternative routes
- Extra time and budget information for alternatives
- Web-based Flask interface

---

## How the System Works

1. The user selects a source and destination.
2. The user provides a maximum travel budget.
3. The user provides a maximum travel time.
4. The user selects the transportation modes available to them.
5. The system identifies connected paths between the source and destination.
6. Different transportation modes are evaluated for each segment of a path.
7. Routes exceeding the user's time or budget constraints are filtered out.
8. Dominated routes are removed based on travel time, cost, and CO₂ emissions.
9. Up to three meaningful feasible routes are selected.
10. A balanced route is recommended using travel time, cost, and CO₂ emissions.
11. If no route satisfies the user's constraints, the system provides closest alternative routes and shows the additional time and budget required.

---

## Recommendation Approach

The recommendation system evaluates each feasible journey using three primary factors:

- **Total Travel Time**
- **Total Cost**
- **Total CO₂ Emissions**

Routes that are worse than another route across all three metrics are considered dominated and removed.

The remaining routes are ranked using a combined recommendation score. The route with the lowest score is presented as the recommended option because it provides a balanced combination of travel time, cost, and CO₂ emissions among the available feasible routes.

---

## No-Feasible-Route Handling

If no route satisfies both the user's maximum travel time and maximum budget, the system does not present an infeasible route as a valid recommendation.

Instead, it provides closest alternative routes and displays:

- Actual travel time
- Actual cost
- CO₂ emissions
- Extra time required
- Extra budget required

This allows users to understand how far the alternatives are from their original constraints.

---

## Dataset

The project uses a synthetic multimodal mobility dataset containing estimated transportation information for connected urban locations.

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

## Technologies Used

- Python
- Pandas
- NumPy
- Flask
- HTML
- CSS
- Jupyter Notebook
- GitHub

---

## Project Structure

```text
ai-sustainable-multimodal-route-planner/
│
├── app.py
├── README.md
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

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Navigate to the Project Directory

```bash
cd ai-sustainable-multimodal-route-planner
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application

```bash
python app.py
```

### 5. Open the Application

Open the local Flask address displayed in the terminal, typically:

```text
http://127.0.0.1:5000/
```

---

## Responsible AI

The project incorporates responsible AI considerations by:

- Providing transparent route metrics.
- Explaining why a route is recommended.
- Clearly distinguishing feasible routes from infeasible alternatives.
- Using synthetic and estimated prototype data.
- Avoiding unnecessary collection of personal or sensitive information.
- Providing users with route information rather than making hidden decisions on their behalf.

---

## Limitations

This is a prototype designed to demonstrate the route planning and recommendation concept.

Current limitations include:

- Transportation values are synthetic or estimated for prototype purposes.
- The system does not use live traffic information.
- The system does not use live public transportation data.
- The system does not provide live GPS navigation.
- The system does not support booking or payment.
- CO₂ values are estimated for prototype evaluation.
- The prototype currently focuses on a predefined transportation network.

---

## Future Enhancements

Potential future improvements include:

- Integration with real-time transportation data
- Live traffic information
- Map-based route visualization
- User-selected optimization priorities for time, cost, or CO₂
- More detailed carbon-emission estimation
- Support for larger transportation networks
- Expansion to additional cities
- Real-time route updates

---

## Project Status

**Completed Prototype**

This project was developed as part of the **1M1B AI for Sustainability Virtual Internship**.

The prototype demonstrates a data-driven approach to sustainable multimodal route planning, helping users compare transportation options based on time, cost, and environmental impact.

---

## Sustainability Impact

The project encourages consideration of environmental impact alongside traditional travel factors such as time and cost.

By presenting multimodal alternatives and CO₂ information, the system aims to support more informed and sustainability-conscious urban travel decisions.