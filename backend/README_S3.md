# S3 integration helper

This file explains how to upload media to S3 and how to use the bundled management command.

1) Prerequisites
- AWS credentials available as environment variables: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
- `AWS_STORAGE_BUCKET_NAME` must be set to your S3 bucket name.
- Install dependencies (`boto3` is already listed in `requirements.txt`).

2) Using the management command locally
From the `backend` folder or project root (where `manage.py` is located) run:

```bash
# make sure AWS env vars are set (powershell example)
$env:AWS_ACCESS_KEY_ID="YOUR_ID"
$env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
$env:AWS_DEFAULT_REGION="eu-north-1"

# run the command and make uploaded objects public
python manage.py upload_media_s3 --public
```

3) Using the command in Railway (recommended for production)
- Add these variables in Railway Environment: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`.
- In Railway Deployments → Console (Run Command), run:

```bash
python manage.py upload_media_s3 --public
```

This will upload contents of `MEDIA_ROOT` into the S3 bucket. The command preserves relative paths (e.g. `hero/...`, `certificates/...`).

4) Notes
- The command uses `boto3` and will respect IAM permissions assigned to the AWS credentials.
- `--public` sets objects ACL to `public-read`. Alternatively, configure a bucket policy for public reads.

