# Privacy Policy & Data Handling

## Overview

This WiFi Indoor Positioning system is designed with privacy as a core principle. All data is stored and processed locally on your device.

## Data Collection

### What We Collect

- WiFi signal strength (RSSI) measurements
- Access point MAC addresses and SSIDs
- Estimated location coordinates
- Movement patterns and velocity
- System configuration and preferences

### What We DON'T Collect

- Personal identification information
- Audio or video recordings
- Internet browsing history
- Application usage data
- Device identifiers that cannot be anonymized

## Data Storage

### Local Storage (Default)

- All data stored in encrypted SQLite database
- Database encryption enabled by default
- No automatic cloud uploads
- Full user control over data deletion

### Cloud Storage (Optional)

- Cloud sync is **disabled by default**
- Requires explicit user opt-in
- User can export and delete data at any time
- No third-party access without consent

## Data Retention

- Signal measurements: 90 days (configurable)
- Location history: 90 days (configurable)
- Calibration data: Until explicitly deleted
- User preferences: Indefinite until deleted

## User Rights

### Data Access

You can:
- Export all collected data in JSON format
- View all stored measurements and predictions
- Access the database directly

### Data Deletion

You can:
- Delete all data with one click
- Delete specific date ranges
- Clear calibration history
- Reset system to factory defaults

### Data Portability

- Export in standard JSON format
- Transfer to another device
- Share with researchers (with consent)

## Security Measures

### Database Security

- AES-256 encryption (when enabled)
- Secure password hashing (bcrypt)
- SQL injection prevention
- No credentials in logs

### Network Security

- WebSocket encryption (TLS/SSL ready)
- API authentication tokens
- CORS protection
- Rate limiting

### Code Security

- Regular dependency updates
- No hardcoded secrets
- Input validation
- Error message sanitization

## User Consent

When using this system, you explicitly consent to:
- Collection of WiFi signal data
- Processing for localization
- Local storage of data
- Use for training ML models

You can revoke consent at any time by:
- Disabling the system
- Deleting your data
- Uninstalling the application

## Third-Party Services (Optional)

This system **does not** require any third-party services by default. Optional features:

- **Cloud Sync**: AWS S3, Google Cloud, etc. (disabled by default)
- **Analytics**: Sentry, Datadog (disabled by default)
- **Updates**: GitHub Releases (optional)

All third-party integrations require explicit permission.

## Children's Privacy

This system is not designed for children under 13. If you are under 13, please get parental consent before using.

## Policy Changes

We will notify users of significant policy changes via:
- In-app notifications
- Email (if enabled)
- GitHub announcements

## Contact

For privacy concerns:
- Open an issue on GitHub
- Email: privacy@example.com

## Compliance

This system aims to comply with:
- GDPR (General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- Local privacy regulations

## Disclaimer

This system is provided as-is. Users are responsible for:
- Complying with local regulations
- Informing people being tracked
- Proper system configuration
- Regular data backups

---

**Last Updated**: May 2026
**Version**: 1.0
