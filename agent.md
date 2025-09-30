# Knowledge Base Agent Documentation

## Project Overview

This Django-based knowledge base application serves as a comprehensive content management and collaboration platform. It provides a centralized repository for technical documentation, articles, and knowledge sharing with built-in moderation and user management capabilities.

## Architecture

### Core Technology Stack
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Frontend**: Bootstrap 5 with Font Awesome icons
- **Database**: SQLite (development) / PostgreSQL (production)
- **Static Files**: Django's static files handling
- **Media Management**: File uploads and PDF handling

### Project Structure
```
knowledge_base/
├── accounts/          # User management and authentication
├── books/            # PDF book library management
├── knowledge/        # Core knowledge base functionality
├── moderation/       # Content moderation system
├── templates/        # HTML templates for all apps
├── static/          # CSS, JavaScript, and static assets
├── media/           # User-uploaded files and PDFs
└── bat/             # Windows batch scripts for automation
```

## Applications and Modules

### 1. Accounts App (`accounts/`)
**Purpose**: User management and authentication system

**Key Features**:
- Simplified registration (Name, Lastname, Username only - email optional)
- Three user roles: User, Editor, Administrator
- Profile management and user dashboard
- User search and listing functionality

**Models**:
- Custom User model extending Django's base user
- Role-based permissions system

### 2. Knowledge App (`knowledge/`)
**Purpose**: Core knowledge base functionality

**Key Features**:
- Article creation and management with rich text editor
- Category-based organization with icons and colors
- Cyrillic-friendly URL slugs
- Article favorites and view tracking
- Search functionality
- Comment system

**Models**:
- `Category`: Hierarchical content organization
- `Article`: Main content with versioning and metadata
- `ArticleView`: View tracking for analytics
- `ArticleAttachment`: File attachments for articles

### 3. Books App (`books/`)
**Purpose**: PDF library management

**Key Features**:
- PDF book upload and management
- Category and tag-based organization
- Book reading interface
- File storage in `media/books/pdfs/`

### 4. Moderation App (`moderation/`)
**Purpose**: Content moderation and suggestion system

**Key Features**:
- User suggestions for new content
- Notification system for moderators
- Approval/rejection workflow
- Moderation dashboard

## Key Technical Features

### Content Management
- **Rich Text Editor**: CKEditor integration for article creation
- **File Uploads**: Support for attachments and PDF books
- **SEO-Friendly URLs**: Automatic slug generation with Cyrillic support
- **Search**: Full-text search across articles and categories
- **Versioning**: Article update tracking

### User Experience
- **Responsive Design**: Bootstrap-based mobile-friendly interface
- **Internationalization**: Russian language support throughout
- **Role-Based Access**: Different permission levels for user types
- **Dashboard**: Personalized user dashboards with statistics

### Development Tools
- **Automation Scripts**: Comprehensive Windows batch scripts in `bat/` folder
- **Database Management**: Automated migration and setup scripts
- **Development Helpers**: Debug utilities and data creation tools

## Configuration Management

### Environment Configuration
- **Settings**: Multiple configuration files for different environments
  - `settings.py`: Development settings
  - `settings_prod.py`: Production configuration
  - `settings_offline.py`: Offline deployment settings
- **Environment Variables**: Using python-decouple for configuration
- **Security**: Proper secret key and debug flag management

### Deployment Options
1. **Standard Development**: Virtual environment with pip
2. **Docker**: Container-based deployment with docker-compose
3. **Offline Deployment**: Air-gapped server deployment capability
4. **Windows Automation**: Batch scripts for quick setup

## Data Models and Relationships

### Core Models
```python
# Category hierarchy for content organization
Category
├── name, slug, description
├── icon, color (UI customization)
├── order (for sorting)
└── Articles (many-to-many relationship)

# Article content management
Article
├── title, slug, content (rich text)
├── author (User foreign key)
├── category (many-to-many to Category)
├── status (draft, published, archived)
├── metadata (created_at, updated_at, views)
└── attachments (related ArticleAttachment)

# User management
User (Custom)
├── username, first_name, last_name
├── email (optional)
├── role (user, editor, admin)
└── profile information
```

### Key Relationships
- Users create Articles (one-to-many)
- Articles belong to Categories (many-to-many)
- Articles can have Attachments (one-to-many)
- Users can moderate Suggestions (one-to-many)

## Security and Permissions

### Authentication
- Django's built-in authentication system
- Custom user model for flexibility
- Session-based authentication for web interface
- API authentication via DRF

### Authorization
- Role-based permissions:
  - **Users**: Read access, comment, create suggestions
  - **Editors**: Create/edit articles, moderate suggestions
  - **Administrators**: Full system access
- Object-level permissions for article editing
- CORS configuration for API access

## Development Workflow

### Setup and Installation
1. **Automated Setup**: Use `install.bat` for Windows quick start
2. **Manual Setup**: Virtual environment + pip install requirements
3. **Database**: SQLite for development, PostgreSQL for production
4. **Initial Data**: `init_project` management command for test data

### Common Development Tasks
- **Database Reset**: `reset-database.bat` for clean start
- **Server Start**: `start.bat` or `python manage.py runserver`
- **Migrations**: Automated in setup scripts
- **Testing**: Built-in Django test framework

## API and Integration

### Django REST Framework
- RESTful API endpoints for all major models
- Serializers for data transformation
- ViewSets for CRUD operations
- API documentation and browseable interface

### Frontend Integration
- AJAX-based interactions for enhanced UX
- Bootstrap components for consistent UI
- Font Awesome icons for visual elements
- Custom JavaScript for dynamic features

## Deployment and Operations

### Production Considerations
- **Static Files**: Collected and served efficiently
- **Media Files**: Proper handling of user uploads
- **Database**: PostgreSQL recommended for production
- **Security**: Environment-based configuration management

### Monitoring and Maintenance
- **Logging**: Django's logging framework
- **Database Backups**: SQLite for development, PostgreSQL dumps for production
- **Updates**: Migration-based database updates
- **Performance**: View tracking and analytics

## Usage Examples

### Creating Content
1. Admin creates categories with appropriate icons/colors
2. Editors create articles using the rich text editor
3. Articles are automatically organized by category
4. Users can search, favorite, and comment on articles

### Content Moderation
1. Users submit suggestions for new content
2. Moderators receive notifications
3. Suggestions are reviewed and approved/rejected
4. Approved content is integrated into the knowledge base

### User Management
1. Simple registration with minimal required fields
2. Role assignment by administrators
3. Profile management and customization
4. Activity tracking and analytics

## Future Extensibility

The application is designed for easy extension with:
- Additional content types through new Django apps
- API integration with external systems
- Advanced search capabilities (Elasticsearch integration)
- Multi-language support expansion
- Advanced analytics and reporting features

This knowledge base system provides a robust foundation for organizational knowledge management with a focus on simplicity, usability, and maintainability.