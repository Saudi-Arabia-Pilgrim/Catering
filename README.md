# Hajj & Umrah Management Platform

## 🌟 Overview

Welcome to the Hajj & Umrah Management Platform! This enterprise-grade solution streamlines the entire process of managing religious travel services, from initial booking to financial reporting. Our platform serves as a central hub connecting travel agencies, hotels, and catering services while providing robust financial insights.

## 🎯 Core Features

- **Smart Booking Management**: Automated room allocation and group management
- **Dynamic Pricing Engine**: Real-time price adjustments based on market conditions
- **Integrated Catering System**: Complete food service management with inventory tracking
- **Financial Analytics**: Comprehensive reporting and business intelligence
- **Staff & Event Coordination**: Streamlined resource management

## 📊 System Architecture

Below is our complete platform workflow showing how different components interact:
```mermaid
graph TB
    %% Authentication Flow
    unAuth["UnAuthenticated User"] --> Authorization
    Authorization --> Register
    Register --> HomePage["Home Page"]
    
    %% Main Management Paths
    HomePage --> Hotels
    HomePage --> Catering
    
    %% Hotel Management Flow
    subgraph HotelManagement
        Hotels --> CheckRole["Check Role"]
        CheckRole --> CEO
        CheckRole --> Manager
        CheckRole --> Staff
        
        CEO --> |Manages| Clients
        CEO --> |Oversees| Partners
        CEO --> |Analyzes| Statistics
        CEO --> |Receives| Notification
        
        Manager --> |Controls| Rooms
        Manager --> |Reviews| Financial
        Manager --> |Manages| Personal["Staff Management"]
        
        Staff --> |Handles| Rooms
        Staff --> |Interacts with| Clients
        Staff --> |Checks| Notification
    end
    
    %% Catering Management Flow
    subgraph CateringManagement
        Catering --> CateringCheckRole["Check Role"]
        CateringCheckRole --> CateringManager
        CateringCheckRole --> CateringStaff
        
        CateringManager --> |Manages| Personal
        CateringManager --> |Oversees| Financial
        CateringManager --> |Controls| Warehouse
        CateringManager --> |Interacts with| Partners
        CateringManager --> |Analyzes| Statistics
        CateringManager --> |Receives| Notification
        
        CateringStaff --> |Manages| Warehouse
        CateringStaff --> |Creates| MenuCreation["Menu"]
        CateringStaff --> |Interacts with| Clients
        CateringStaff --> |Checks| Notification
        
        MenuCreation --> MenuDetailsCost["Menu Details & Cost"]
        MenuDetailsCost --> Ingredients["Ingredient Management"]
    end
    
    %% Styling
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef process fill:#e1f3fd,stroke:#333,stroke-width:1px
    classDef financial fill:#e1fde3,stroke:#333,stroke-width:1px
    
    class unAuth,HomePage,Hotels,Catering,Rooms,Clients,Partners,Statistics,Notification default
    class Authorization,Register,CEO,Manager,Staff,CateringManager,CateringStaff process
    class Financial,Personal,Warehouse,MenuCreation,Ingredients financial
```

## 📊 Business Logic Flowchart
```mermaid
flowchart TB
    Start["Client Requests (Hajj/Umrah)"]
    Agencies["Travel Agencies"]
    Request["Agency Request:\n- Group Size\n- Duration"]
    Admin["Admin Panel\n(Manage Partners, Bookings, Reports)"]
    
    %% Main process branches
    RoomAlloc["Dynamic Room Allocation"]
    FoodCalc["Dynamic Food Calculation"]
    PartnerMgmt["Partner Hotel Management"]
    StaffMgmt["Staff Management\n(Scheduling, Payroll)"]
    EventMgmt["Event Management"]
    
    %% Room allocation branch
    PartnerHotels["Partner Hotels"]
    BookingConf["Booking Confirmation"]
    ProfitReports["Profit & Performance Reports"]
    DetailedReports["Detailed Reports:\n- Partner Profits\n- Costs"]
    
    %% Food calculation branch
    Catering["Catering Services\n(Food Menu, Pricing)"]
    Warehouse["Warehouse:\n- Track Ingredients\n- Costs & Stock"]
    DynamicPricing["Dynamic Pricing:\n- Hotels\n- Catering"]
    SupplyChain["Supply Chain:\n- Vendor Management\n- Ingredient Costs"]
    
    %% Financial branch
    FinanceMgmt["Finance Management\n(Costs, Profit, Recurring Revenue)"]
    FinInsights["Financial Insights:\n- Monthly Recurring Revenue\n- Cost Analysis"]
    
    %% Define connections
    Start --> Agencies
    Agencies --> Request
    Request --> Admin
    
    %% Admin panel connections
    Admin --> RoomAlloc
    Admin --> FoodCalc
    Admin --> PartnerMgmt
    Admin --> StaffMgmt
    Admin --> EventMgmt
    
    %% Room allocation flow
    RoomAlloc --> PartnerHotels
    PartnerHotels --> BookingConf
    BookingConf --> ProfitReports
    ProfitReports --> DetailedReports
    
    %% Food calculation flow
    FoodCalc --> Catering
    Catering --> Warehouse
    Warehouse --> DynamicPricing
    Warehouse --> SupplyChain
    Catering --> SupplyChain
    
    %% Financial flow
    DetailedReports --> FinanceMgmt
    FinanceMgmt --> FinInsights
    
    %% Styling
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef process fill:#e1f3fd,stroke:#333,stroke-width:1px
    classDef financial fill:#e1fde3,stroke:#333,stroke-width:1px
    
    class Start,Agencies,Request default
    class RoomAlloc,FoodCalc,PartnerMgmt,StaffMgmt,EventMgmt process
    class FinanceMgmt,FinInsights,DetailedReports,ProfitReports financial
```

## 🚀 Getting Started

## 📦 Dependency Management

Our project uses a structured approach to managing dependencies across different environments:

### 📄 Requirements Files Structure

- **`base.txt`**:
  - Core dependencies required across all environments.
  - Foundation for all other requirement files.
  - Contains essential packages for basic functionality.

- **`dev.txt`**:
  - Developer-specific tools and libraries.
  - Extends `base.txt`.
  - Includes debugging tools and development utilities.
  - Recommended for local development.

- **`test.txt`**:
  - Testing-related dependencies.
  - Extends `base.txt`.
  - Contains testing frameworks and assertion libraries.
  - Used in CI/CD pipelines.

- **`prod.txt`**:
  - Production-specific dependencies.
  - Extends `base.txt`.
  - Includes optimized libraries and production servers.
  - Example: gunicorn, optimized database connectors.

- **`local.txt`** *(Optional)*:
  - For local overrides or private dependencies.
  - Extends `dev.txt`.
  - Perfect for team-specific or developer-specific packages.
  - Not tracked in version control.


### Prerequisites

- Python 3.12+
- Django 5.1.3+
- PostgresSQL 16+
- Redis 5.2.0+

### Installation

1. Clone the repository:
```bash
git clone git@github.com:Saudi-Arabia-Pilgrim/Catering.git
cd catering
```

2. Set up the virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements/dev.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Start development servers:
```bash
# Terminal 1: Backend
python manage.py runserver
```

## 👥 Team Structure & Responsibilities

### Project Management
- **Project Manager**: Mukhsin Mukhtorov
  - Strategic planning and roadmap development
  - Sprint planning and backlog grooming
  - Stakeholder communication
  - Resource allocation

### Development Teams

#### Backend Team
- **Lead**: Oybek Yo'ldoshev
- **Responsibilities**:
  - Core API development
  - Database optimization
  - Service integration
  - Performance monitoring

#### Frontend Team
- **Lead**: Alisher
- **Responsibilities**:
  - User interface development
  - Component library maintenance
  - Responsive design implementation
  - Performance optimization

#### DevOps Team
- **Lead**: Mukhsin Mukhtorov
- **Responsibilities**:
  - CI/CD pipeline management
  - Infrastructure maintenance
  - Security implementation
  - Monitoring and alerts


## 📅 Sprint Schedule

We operate in 2-week sprints with the following recurring events:

- **Sprint Planning**: Monday (Sprint Start) - 10:00 AM
- **Daily Standups**: Every weekday - 18:30 PM
- **Sprint Review**: Friday (Sprint End) - 2:00 PM
- **Sprint Retrospective**: Friday (Sprint End) - 3:30 PM

## 🔄 Development Workflow

1. **Branch Naming Convention**:
   - Feature: `feature/JIRA-123-short-description`
   - Bugfix: `bugfix/JIRA-123-short-description`
   - Hotfix: `hotfix/JIRA-123-short-description`


2. **Commit Message Format**:
```
[JIRA-123] Category: Brief description

- Detailed bullet points
- Of changes made
```

3. **Pull Request Process**:
   - Create PR with template
   - Assign reviewers
   - Pass CI checks
   - Obtain 2 approvals
   - Merge using ```merge pull request```

## 📈 Monitoring & Performance

- Application Performance: New Relic
- Error Tracking: Sentry
- Log Management: ELK Stack
- Uptime Monitoring: Pingdom

## 🔒 Security & Compliance

- Regular security audits
- OWASP compliance
- Data encryption at rest and in transit
- Regular penetration testing
- GDPR compliance measures

## 🎯 Current Sprint Goals (Sprint 1)

1. Implement dynamic pricing algorithm
2. Optimize room allocation system
3. Enhance reporting dashboard
4. Implement multi-language support

## 📞 Support & Contact

- **Technical Issues**: Create a GitHub issue
- **Security Concerns**: ```mukhsinmukhtorov@arizona.edu```
- **Emergency Contact**: +998993233528

## 👥 Contributors

We believe in the power of collaboration. Below are some of our amazing contributors:

| Name                                                | LinkedIn                                                             | Project Spent Time                                                                                                                       |
|-----------------------------------------------------|----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------| 
| [Mukhsin Mukhtorov](https://github.com/Mukhsin0508) | [LinkedIn](https://www.linkedin.com/in/mukhsin-mukhtorov-58b26221b/) | ![Wakatime Badge](https://wakatime.com/badge/user/60731bfe-5801-4003-b6ab-b7db12ed73d0/project/e1974447-198b-4e5c-b175-201c8be81c13.svg) |



## 📝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License

This project is licensed under the No Licenses - see the [LICENSE.md](LICENSE) file for details.

---

*Last updated: November 18, 2024*
