edo-system/
├── .github/
│   └── workflows/
│       ├── deploy.yaml
│       ├── production.yaml
│       └── staging.yaml
│
├── docs/
│   ├── architecture.md
│   ├── architecture-diagram.png
│   ├── deployment.md
│   ├── folder-structure.md
│   └── sequence-diagram.png
│
├── frontend/
│   ├── assets/
│   ├── scripts/
│   ├── styles/
│   ├── favicon.ico
│   ├── favicon.png
│   └── index.html
│
├── infrastructure/
│   ├── .aws-sam/
│   ├── parameters/
│   ├── scripts/
│   ├── services/
│   │   ├── delete-failed-order-service/
│   │   ├── failed-orders-service/
│   │   ├── get-orders-service/
│   │   ├── ingestion-service/
│   │   └── inventory-worker/
│   ├── samconfig.toml
│   ├── sns-publish.json
│   ├── sns-topic-policy.json
│   └── template.yaml
│
├── shared/
│   ├── logging.py
│   ├── models.py
│   └── utils.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_utils.py
│   └── test_worker.py
│
├── .gitignore
├── EDO_project_doc.md
└── README.md