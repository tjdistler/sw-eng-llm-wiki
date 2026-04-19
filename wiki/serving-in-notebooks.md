# Serving Data in Notebooks

**Summary**: Jupyter notebooks (and successors like JupyterLab) are the dominant interactive interface for data scientists — for exploration, feature engineering, and model training. Chapter 9 frames the DE's role as ensuring safe, scalable data access into notebooks: credential hygiene, access controls, and a path off the laptop when datasets outgrow local memory.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## The notebook as a serving target

Data scientists routinely connect notebooks to external sources — APIs, databases, warehouses, lakes, object stores — via built-in or imported client libraries. Notebooks need:

- **Correct credentials** to authenticate against the source.
- **Appropriate row/column access** to the tables or files.
- **Scalable compute** when the data outgrows the laptop.

Chapter 9: "The data engineer will often assist the data scientist in finding the right data, and then ensure that they have the right permissions to access the rows and columns required" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## The credential-handling hazard

Chapter 9 dedicates a warning box to this and it's worth repeating (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- Credentials get embedded directly in notebook code.
- Credentials leak into version-control repositories.
- Credentials get passed around in email and chat.

The DE's job is to audit notebook security practices and push for alternatives: "credentials should never be embedded in code; ideally, data scientists use credential managers or CLI tools to manage access." Chapter 9 observes that data scientists are "highly receptive to these conversations if they are given alternatives."

## The "pandas ran out of memory" scaling arc

Chapter 9 walks through the standard data-scientist-outgrows-laptop migration (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

1. **Local notebook + pandas.** Load a CSV; store in memory. Works until dataset > RAM.
2. **Cloud-based notebook.** Storage and memory flexibly scale. Buys time.
3. **Distributed execution.** Dask, Ray, or Spark for Python-based scaling.
4. **Cloud-managed ML platform.** Amazon SageMaker, Google Cloud Vertex AI, Azure ML — end-to-end managed offerings.
5. **Open-source end-to-end.** Kubeflow (Kubernetes), MLflow (Spark-centric).

The DE's role: "get data scientists off their laptops and take advantage of the cloud's power and scalability." Set up cloud infrastructure, manage environments, train data scientists in cloud-based tools.

## "Data science ops"

Chapter 9 observes the cloud-move requires significant operational work — version management, access control, SLAs — and when done well, creates large payoff. Essentially, [[dataops|DataOps]] applied to the data science workflow (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Productionised notebooks

Chapter 9 calls out a controversial but widely-adopted pattern: running notebooks in production (Netflix is named) (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

Trade-offs:

- **Pro** — data scientists ship to production much faster; less rewriting by DE/MLE.
- **Con** — notebooks are "inherently a substandard form of production" — poor reproducibility, weak testing, implicit cell-execution order.
- **Hybrid middle ground** — notebooks for light production; full productionisation for high-value projects.

## The DE's job in one sentence

"Data engineers and ML engineers play a key role in facilitating the move to scalable cloud infrastructure." Set up the environments, run credential and access governance, and make the transition from laptop to cluster smooth enough that data scientists don't dread it (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Cross-book connections

- **[[dataops]]** — the discipline Chapter 9's "data science ops" extends to the notebook surface.
- **[[data-security]]** / **[[least-privilege]]** — notebook credential hygiene is a direct application.

## Related pages

- [[data-serving]]
- [[feature-store]]
- [[data-security]]
- [[least-privilege]]
- [[dataops]]
- [[feature-engineering]]
- [[data-science-hierarchy-of-needs]]
