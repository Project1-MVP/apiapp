# Project Stucture
project/
│
├── ims/                            # Inventory Management Service
│   ├── __init__.py
│   ├── main.py                     # FastAPI app for IMS
│   ├── routes/                     # IMS API routes
│   │   ├── __init__.py
│   │   └── sample.py               # Example IMS route
│   ├── models/                     # Database models specific to IMS
│   │   ├── __init__.py
│   │   └── inventory.py
│   ├── schemas/                    # Pydantic schemas for IMS
│   │   ├── __init__.py
│   │   └── inventory.py
│   ├── services/                   # Business logic for IMS
│   │   ├── __init__.py
│   │   └── inventory.py
│   ├── dependencies.py             # Dependencies and common utilities for IMS
│   └── utils.py                    # Helper functions for IMS
│
├── oms/                            # Order Management Service
│   ├── __init__.py
│   ├── main.py                     # FastAPI app for OMS
│   ├── routes/                     # OMS API routes
│   │   ├── __init__.py
│   │   └── sample.py               # Example OMS route
│   ├── models/                     # Database models specific to OMS
│   │   ├── __init__.py
│   │   └── orders.py
│   ├── schemas/                    # Pydantic schemas for OMS
│   │   ├── __init__.py
│   │   └── orders.py
│   ├── services/                   # Business logic for OMS
│   │   ├── __init__.py
│   │   └── orders.py
│   ├── dependencies.py             # Dependencies and common utilities for OMS
│   └── utils.py                    # Helper functions for OMS
│
├── admin/                          # Admin APIs
│   ├── __init__.py
│   ├── main.py                     # FastAPI app for Admin APIs
│   ├── routes/
│   │   ├── __init__.py
│   │   └── admin.py                # Routes for managing tenants and users
│   ├── models/
│   │   ├── __init__.py
│   │   └── admin.py                # Admin-specific models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── admin.py                # Admin-specific schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── admin.py                # Admin-specific business logic
│   ├── dependencies.py
│   └── utils.py
│
├── core/                           # Shared components
│   ├── __init__.py
│   ├── config.py                   # Configuration settings
│   ├── database.py                 # Database connection and models
│   ├── auth.py                     # Auth-related utilities and middleware
│   ├── rls.py                      # Row-Level Security implementation
│   └── schemas/                    # Shared Pydantic schemas
│       ├── __init__.py
│       └── user.py                 # User and Tenant schemas
│
├── migrations/                     # Database migrations (e.g., Alembic)
├── tests/                          # Unit and integration tests
│   ├── __init__.py
│   ├── test_ims.py
│   ├── test_oms.py
│   └── test_admin.py
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
├── docker-compose.yml              # Docker Compose configuration
└── README.md                       # Project documentation
