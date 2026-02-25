import argparse
import importlib.util
import json
import os
import sys
import tempfile

# Required so that hover-update can import its local totp
hover_dir = os.path.join(os.path.dirname(__file__), 'hover-dyn-dns')
sys.path.insert(0, hover_dir)

# Required because hover-update is not a package nor is it named properly
spec = importlib.util.spec_from_file_location("hover_updater", "hover-dyn-dns/hover-update.py")
hover_updater = importlib.util.module_from_spec(spec)
sys.modules["hover_updater"] = hover_updater
spec.loader.exec_module(hover_updater)

def build_config_from_env():
    """Build a config dict from env vars that we'll use to make the temp config file"""
    config = {
        "username":           os.environ.get("HOVER_USERNAME", ""),
        "password":           os.environ.get("HOVER_PASSWORD", ""),
        "totp_secret":        os.environ.get("HOVER_TOTP_SECRET", ""),
        "dnsid":              os.environ.get("HOVER_DNS_ID", ""),
        "nakedDomain":        os.environ.get("HOVER_DOMAIN", "default_domain"),
        "discoverip":         os.environ.get("HOVER_DISCOVER_IP", "true"),
        "ipaddress":          os.environ.get("HOVER_IP_ADDRESS", ""),
        "srcdomain":          os.environ.get("HOVER_SRC_DOMAIN", ""),
        "userAgent":          os.environ.get("HOVER_USER_AGENT", "Chromium"),
        "loglevel":           os.environ.get("HOVER_LOG_LEVEL", "INFO"),
        "logRetentionMaxDays": int(os.environ.get("HOVER_LOG_RETENTION_DAYS", "7")),
        "runInterval":        int(os.environ.get("HOVER_RUN_INTERVAL", "300")),
    }
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hover DNS Updater Entrypoint. Use HOVER_ env vars to configure and --getDNSID to get the ID required for running the dns updater.')
    parser.add_argument('--getDNSID', action='store_true', help='Fetch and print DNS IDs for all domains')
    parser.add_help=True
    args = parser.parse_args()
    config = build_config_from_env()
    print(config)
    config_file = tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False, dir='/tmp'
    )
    json.dump(config, config_file)
    config_file.close()

    if args.getDNSID:
        sys.argv = ['hover-update.py', '--loglevel', 'DEBUG', '--getDNSID', '--config', config_file.name]
        hover_updater.main()
        sys.exit(0)

    # our arguments go here since hover-update is trying to grab CLI arguments
    sys.argv = ['hover-update.py', '--config', config_file.name]
    hover_updater.main()

