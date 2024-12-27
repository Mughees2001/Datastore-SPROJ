# A Novel Low Latency Datastore for the Edge


[Click here to Open Paper](docs/paper.pdf)


## Abstract
Computing at the edge has been a key development in networks over the past decade. However, in the mobile computing space, it is still an emerging paradigm with a multitude of use cases in IoT, video analytics, gaming, etc. 

The key idea in edge computing is to reduce computational requirements on devices by offloading compute to the edge. In this project, we aim to solve the problems incurred during stateful application migration using a proposed 5G architecture by creating a novel low-latency datastore to facilitate state migration on the edge.

We develop a new data structure, a hashed queue, and use it to build a datastore. This datastore can be integrated into any 5G control plane design. We also test and evaluate our data structure, eventually implementing a datastore in Python and C++. Our evaluations show that the algorithm removes the need for sorting and provides a 50% reduction in the payload transferred in the best case. We also discuss local and wide-area replication schemes.



## Authors
- **Muhammad Jazlan**
  - *Currently enrolled at University of California, Davis*
  - Affiliation: Lahore University of Management Sciences  
  - Email: [24100022@lums.edu.pk](mailto:24100022@lums.edu.pk)

- **Mughees ur Rehman**
  - *Currently enrolled at Virginia Tech*
  - Affiliation: Lahore University of Management Sciences  
  - Email: [24100086@lums.edu.pk](mailto:24100086@lums.edu.pk)
  - Email : [mughees@vt.edu.pk](mailto@mughees@vt.edu)

---

## Highlights
- **Edge Computing Focus**: Addressing computational challenges for mobile devices in IoT, video analytics, and gaming.
- **Low-Latency Datastore**: Creation of a datastore to facilitate state migration using a hashed queue.
- **5G Control Plane Integration**: Designed to be integrated into a 5G architecture.
- **Efficiency**: Provides a 50% reduction in payload size during stateful application migration.
- **Implementation**: Developed in Python and C++, with testing and evaluation to validate its performance.

---

## Implementation Details
### RapidQueue Algorithm
- A new data structure: *Hashed Queue*.
- Removes the need for sorting, improving latency performance.
- Supports efficient local and wide-area replication schemes.

### Programming Languages Used
- Python
- C++
- C

----

## References
Please see the `reference.bib` file for the full list of references cited in the project.

---

## Appendix
For details about the `RapidQueue Algorithm`, see the appendix provided in the `sections/appendixA` file.
