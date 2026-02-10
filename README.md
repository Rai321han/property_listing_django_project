# Property Listing Application

[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org) [![Django](https://img.shields.io/badge/django-6.0.2-green.svg)](https://www.djangoproject.com)

A Django-based real estate property listing application that allows users to browse, search, and view property listings with location-based filtering and autocomplete functionality.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation & Setup](#installation--setup)
- [App Structure](#app-structure)
- [Database Models](#database-models)
- [Views & URL Routes](#views--url-routes)
- [Features in Detail](#features-in-detail)
- [Admin Interface](#admin-interface)
- [Migration and Data Import](#migration-and-data-import)

## Overview

The Property app is a Django application module that manages property listings, locations, and associated images. It provides a complete system for displaying properties with advanced search and filtering capabilities.

## Key Features

- **Property Listings**: Browse and search available properties
- **Location-based Filtering**: Filter properties by geographic location
- **Autocomplete Search**: Smart location autocomplete with property count
- **Image Management**: Associate multiple images with properties
- **Property Details**: Comprehensive property information including type, price, bedrooms, bathrooms, and status
- **Responsive Design**: Clean HTML templates for property display

## Installation & Setup

### Prerequisites
- Python 3.12 or higher
- Django 6.0.2 or higher

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone https://github.com/Rai321han/property_listing_django_project.git
```

#### 2. Navigate to project directory
```bash
cd property_listing_django_project
```

#### 3. Create Virtual Environment

```bash
# Create and activate virtual environment using uv
uv venv
source .venv/bin/activate
```

#### 4. Install Dependencies
```bash
# uv (recommended)
uv sync

# or

# pip
pip install -r requirements.txt
```

#### 5. Setup Database & Admin

```bash
# Create superuser for admin access
python manage.py createsuperuser
```

#### 6. Load Data & Run Server

```bash
# Start development server
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`


## App Structure

```
property/
├── models/
│   ├── property.py       # Property model - core real estate listing
│   ├── location.py       # Location model - geographic locations
│   └── image.py          # Image model - property images
├── views.py              # View functions and API endpoints
├── urls.py               # URL routing configuration
├── admin.py              # Django admin configuration
├── templates/
│   └── property/
│       ├── base.html               # Base template
│       ├── home.html               # Home page
│       ├── property_list.html      # Property listings page
│       └── property_detail.html    # Property detail page
├── static/
│   ├── css/                    # Stylesheets
│   └── js/
│       └── autocomplete.js     # Location autocomplete functionality
└── migrations/                 # Database migrations
```

## Database Models

### Property
Represents an individual property listing with the following attributes:

- **title**: Property name/title (CharField)
- **description**: Detailed description (TextField)
- **property_type**: Type of property (House, Apartment, Commercial)
- **status**: Current status (Available, Rented)
- **location**: Geographic location (ForeignKey to Location)
- **price**: Property price (DecimalField)
- **bedrooms**: Number of bedrooms (PositiveIntegerField)
- **bathrooms**: Number of bathrooms (PositiveIntegerField)
- **created_at**: Creation timestamp (auto)
- **updated_at**: Last update timestamp (auto)

**Key Properties:**
- `primary_image`: Returns the first associated image
- `formatted_price`: Returns price formatted as currency (e.g., "$150,000.00")

### Location
Represents geographic locations where properties are situated:

- **name**: Location name (unique, indexed)
- **city**: City name
- **state**: State/province (optional)
- **country**: Country (default: USA)
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

**Key Properties:**
- `full_address`: Formatted complete address

### Image
Handles property images:

- **property**: Associated property (ForeignKey)
- **image**: Image file (ImageField)
- **caption**: Optional image caption
- **is_primary**: Mark as primary image for property
- **order**: Display order for multiple images
- **uploaded_at**: Upload timestamp

**Features:**
- Automatically ensures only one primary image per property
- Provides thumbnail URL access
- Ordered display by position and upload date


## Views & URL Routes

### Frontend Pages

#### Home Page (`/`)
- Includes property search input

#### Property List (`/properties`)
- Full list of properties

#### Property Detail (`/properties/<int:pk>`)
- Detailed view of individual property
- Displays all images associated with the property
- Shows complete property information

### API Endpoints

#### Location Autocomplete (`/autocomplete/`)
- **Method**: GET
- **Parameters**: 
  - `q`: Search query (minimum 1 character)
- **Response**: JSON array of location suggestions
- **Features**:
  - Searches property name, city, and country
  - Returns up to 5 suggestions
  - Includes property count for each location
  - Orders by number of available properties

**Example Response:**
```json
{
  "suggestions": [
    {
      "id": 1,
      "name": "Downtown District",
      "city": "New York",
      "country": "USA",
      "full_address": "Downtown District, New York, USA",
      "property_count": 8
    }
  ]
}
```

## Features in Detail

### Search & Filtering
- **Autocomplete Location Search**: Real-time location suggestions with property counts
- **Property Filtering**: Filter by location with support for both location ID and name
- **Status Filter**: View only available or rented properties

### Performance Optimizations
- **Database Indexing**: Indexed fields for location and creation date
- **Query Optimization**: 
  - Uses `select_related()` for efficient ForeignKey lookups
  - Uses `prefetch_related()` for efficient reverse relations

### Property Status Management
Properties can be marked as:
- **Available**: Property is available for rent/purchase
- **Rented**: Property is currently rented

## Admin Interface

The Django admin interface is configured for managing:
- Properties with full CRUD operations
- Locations and their properties
- Property images with ordering

Access via `/admin/` after creating a superuser account.

## Migration and Data Import

Database migration
```bash
# Run migrations
python manage.py migrate
```


The application includes a management command for importing properties:

```bash
python manage.py import_properties <csv_file_path>
```

Expected CSV format with columns: title, description, property_type, status, price, bedrooms, bathrooms

> [!NOTE]
> A sample CSV file containing property data is provided and has already been imported.

## Template Features

All templates include:
- Responsive design for mobile and desktop
- Property image display
- Interactive autocomplete search
- Formatted price display
- Location information

JavaScript enhancement via `search.js` provides real-time location suggestions.

