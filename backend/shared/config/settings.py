from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings - equivalent to appsettings.json + IOptions<T>"""
    
    # API Configuration
    debug: bool = False
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # JWT Configuration
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 30
    
    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    
    # AWS Cognito
    cognito_user_pool_id: str = ""
    cognito_client_id: str = ""
    cognito_client_secret: str = ""
    
    # AWS DynamoDB
    dynamodb_table_galleries: str = "falbo-galleries"
    dynamodb_table_blog: str = "falbo-blog"
    
    # AWS S3
    s3_bucket_name: str = "falbo-images"
    s3_region: str = "us-east-1"
    
    # CORS Settings
    allowed_origins: str = "http://localhost:3000"  # Comma-separated for multiple origins
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance (like IOptions<Settings>)
settings = Settings()
