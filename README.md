# weedeater
## Proposal

Small Selective Herbicide dispenser

## Problem

When liquid herbicides are used in agriculture, much of the active chemical is wasted
(either from over-spray, or application to non-targeted foliage.) Currently, several firms
are developing systems which use visual weed recognition to limit spray application only
to targeted species.
(e.g. https://www.gearbrain.com/weed-killing-robots-reduce-pesticides-2593338605.html

Proposal is to develop a hand-held dispenser which will identify weeds and dispense
appropriate (likely granular) herbicides appropriate to the targeted species. The
intent is to supply this weed recognition technologies to small-holder farmers in lesser
developed countries.

This would give advanced agricultural technology to poor farmers in lesser developed
countries. If linked to cell phone (or other communication technologies), this could also
provide large-area surveillance of weed growth, invasive weed spread, and possibly
even insect populations to national and international agriculture agencies.
A significant secondary benefit of the data link would be that a central agriculture
agency (e.g. government, university, or NGO) Would receive the data and could provide
information and advice to the small-holder farmers- a “Virtual Agricultural Extension
Agent”

## Target User / Customer

Smallholder farmers in developing areas
Secondary: Governments (agriculture departments, NGOs)

## Data
Most of the data used would be generated within the project itself
Reference Weed Identification images
UC weed photo library
Weed Alert (need to verify images are open source)
Weed Science Society of America
Possible data science techniques
CNN (for weed recognition/classification within the unit)
Pub/Sub data handling (MQTT)
General IoT activity of edge sensors feeding central analytic systems.
Reporting and visualization (D3 (or C3 or Chart.js)) visualizations

## Related research/products

Wheeled “smart weeders” noted above
Developing world applications of Raspberry Pi
### Implementation notes:
- May be able to generate our own images by photographing sprouting seeds (i.e. use various
beans, peas, and flower seeds as sample “crop” and “weed” plants as a training example)
- May identify low cost peristaltic pumps for applying liquid agents (example below)

