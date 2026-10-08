# ClinScribe AI — Security

## Overview

ClinScribe AI treats all healthcare data as sensitive. This document describes the security architecture and measures implemented.

## Authentication

- **JWT-based authentication** with configurable expiration
- **bcrypt password hashing** for credential storage
- **Bearer token** scheme for API access
- Session timeout after configurable period of inactivity

## Authorization

- **Role-based access control (RBAC)**: Doctor, Nurse, Admin, Staff
- Doctors can only access their own patients' data
- Administrative functions restricted to Admin role
- API endpoints enforce role checks

## Data Protection

### In Transit
- HTTPS/TLS encryption for all API communication
- Secure WebSocket connections for live streaming

### At Rest
- Database encryption configurable via environment variable
- Audio files stored temporarily and configurable retention
- Sensitive fields can be encrypted at application layer

### Data Retention
- Configurable retention period (default: 90 days)
- Automatic cleanup of temporary audio files
- Audit trail preserved independently

## Audit Logging

Every significant action is logged:
- User authentication (login/logout)
- Patient data access
- Consultation creation/modification
- Clinical note creation/editing/approval
- FHIR data export
- Settings changes

Audit log fields:
- User ID
- Action type
- Resource type and ID
- Timestamp
- IP address
- User agent

## API Security

- **Input validation**: All inputs validated via Pydantic schemas
- **CORS configuration**: Restricted to known frontend origins
- **Rate limiting**: Configurable (recommended for production)
- **No raw stack traces**: User-friendly error messages

## Clinical Data Safety

- AI output is always marked as "AI_GENERATED"
- No AI output becomes final without doctor approval
- Version history maintained for all clinical notes
- Evidence links preserve traceability

## Privacy Center

The application includes a Privacy Center dashboard showing:
- Recording consent status
- Raw audio storage policy
- Data retention configuration
- Access control status
- Audit log status

## Known Limitations (Hackathon Prototype)

- JWT secret key should be rotated for production
- Rate limiting not yet implemented
- End-to-end encryption not yet implemented
- HIPAA/ABDM compliance requires additional measures
- Password complexity rules not enforced in demo mode
- Session management is basic (JWT expiry only)

## Recommendations for Production

1. Implement end-to-end encryption
2. Add rate limiting and DDoS protection
3. Implement IP whitelisting for admin endpoints
4. Add multi-factor authentication
5. Conduct security audit and penetration testing
6. Implement HIPAA/ABDM compliance measures
7. Add data anonymization for analytics
8. Implement key rotation
9. Add intrusion detection
10. Conduct regular security assessments
