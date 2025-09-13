# Infrastructure Overview

## CI/CD Platform

**GitHub Actions** (replaces Azure DevOps Pipelines)

- Build and test automation
- Deployment orchestration
- Integration with AWS services

## Infrastructure as Code

**AWS CDK (Python)** (replaces ARM/Bicep)

- Type-safe infrastructure definitions
- Familiar programming approach
- Good Python integration

## Deployment Architecture

### Frontend

- **Vercel** or **S3 + CloudFront**
- Static site hosting
- Global CDN distribution

### Backend  

- **AWS Lambda + API Gateway**
- Serverless Python API
- Auto-scaling and pay-per-use

### Resources

- **DynamoDB** - Gallery metadata storage
- **S3** - Image file storage  
- **Cognito** - User authentication
- **SES** - Email services

## Environment Strategy

### Development

- GitHub → Actions → AWS Dev Environment
- Feature branches deploy to preview environments

### Production  

- Main branch → Actions → AWS Prod Environment
- Manual approval gates for production

## Workflow

```txt
Code Push → GitHub Actions → Tests → Build → Deploy Infrastructure → Deploy Apps
```

```txt
falbo_obscura/
├── .github/
│   └── workflows/
│       ├── ci.yml           # Build/test
│       ├── deploy-dev.yml   # Dev deployment
│       └── deploy-prod.yml  # Prod deployment
├── terraform/               # Infrastructure
│   ├── environments/
│   │   ├── dev/
│   │   └── prod/
│   └── modules/
├── backend/                 # Your FastAPI app
└── frontend/               # Your Next.js app
```
