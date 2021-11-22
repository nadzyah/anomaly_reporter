# Anomaly Reporter

It's a StackStorm pack to orchestrate log anomaly reporting.

# Installation and Usage

**Step 1:** Clone this repo to the local filesystem

**Step 2:** Install the pack

```bash
$ st2 pack install file:///home/user/anomaly_reporter
```

**Step 3:** Create the configuration file `anomaly_reporter.yaml` in the `/opt/stackstorm/configs/` directory:

```yaml
$ cat /opt/stackstorm/configs/anomaly_reporter.yaml
---
mongouri: mongodb://172.17.18.83:27017
sourcedb: anomalydb
clients_emails_and_hosts:
  client1:
    emails:  # Email addresses of the cleint1 admins
      - client1-1@example.com
      - cleint1-2@example.com
    cols_and_hosts:  # MongoDB collections and devices hostnames
                     # that are interested for client1
      web_anomaly:
        - dataform
      network_anomaly:
        - cumulus
  client2:
    emails:
      - client2-1@example2.com
      - cleint2-2@example2.com
    cols_and_hosts:
      utm_anomaly:
      - 172.17.18.56
      network_anomaly:
        - cumulus
event_handler_period: 1
report_store_dir: "/opt/reports/"
smtp_servername: mail.solidex.by
smtp_server_port: 465
use_ssl: true
use_starttls: false
sender: reporter@solidex.by
sender_username: ""
sender_password: ""
```

Configuration parameters:

<table>
  <thead>
    <tr>
      <th>Config field</th>
      <th>Details</th>
    </tr>
  </thead>
  <tbody> 
  <tr>
    <td>mongouri</td>
    <td>The dictionary of clients and collections with hosts that are accosiated
        with each client. Use the specified in the example format</td>
  </tr>
  <tr>  
  <tr>
    <td>mongouri</td>
    <td>MongoDB server URI in "mongodb://username:password@X.X.X.X:yyyy" format </td>
  </tr>
  <tr>
     <td>sourcedb</td>
     <td>Name of the database, where anomaly logs are stored</td>
  </tr>
  <tr>
     <td>report_store_dir</td>
     <td>Base directory, where reports will be stored. MUST contain a slash at the end</td>
  </tr>
  <tr>
     <td>smtp_servername</td>
     <td>The mail server FQDN</td>
  </tr>
  <tr>
     <td>use_ssl</td>
     <td>True if SSL/TLS (not STARTTLS) encryption should be used</td>
  </tr>
  <tr>
     <td>use_starttls</td>
     <td>True if STARTTLS should be used</td>
  </tr>
  <tr>
     <td>sender</td>
     <td>The sender email (e.g. reporter@example.com)</td>
  </tr>
  <tr>
     <td>sender_username</td>
     <td>The sender username for SMTP authentication. Use "" if authentication is not required</td>
  </tr>
  <tr>
     <td>sender_password</td>
     <td>The sender password for SMTP authentication. Use "" if authentication is not required</td>
  </tr>
  </tbody>
</table>

**Step 4:** Register the pack and the config file
```bash
$ sudo st2ctl reload --register-all
```

