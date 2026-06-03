"""
Reward Script: Kubernetes Helm chart deployment configuration
Task ID: os_gff_094
Domain: os (filesystem / Helm chart)
Scoring:
  - Component 1: Chart structure (Chart.yaml, values.yaml, templates/) — 0.15
  - Component 2: Required template files exist — 0.15
  - Component 3: Chart.yaml correct metadata — 0.10
  - Component 4: values.yaml has required configuration sections — 0.20
  - Component 5: staging-values.yaml overrides replicaCount=2 and ingress.enabled=true — 0.20
  - Component 6: Template files contain valid Helm templating and correct K8s kinds — 0.20
"""

import os
import yaml

WORKDIR = '/opt/helm/myapp'

def verify_task():
    """
    Verify Helm chart deployment task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Chart structure exists (0.15 points)
    # The myapp/ directory with Chart.yaml, values.yaml, and templates/ must exist
    try:
        chart_yaml_exists = os.path.isfile(os.path.join(WORKDIR, 'Chart.yaml'))
        values_yaml_exists = os.path.isfile(os.path.join(WORKDIR, 'values.yaml'))
        templates_dir_exists = os.path.isdir(os.path.join(WORKDIR, 'templates'))

        if chart_yaml_exists and values_yaml_exists and templates_dir_exists:
            print(f"PASS: Component 1 — Chart structure exists (Chart.yaml, values.yaml, templates/) (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not chart_yaml_exists:
                missing.append('Chart.yaml')
            if not values_yaml_exists:
                missing.append('values.yaml')
            if not templates_dir_exists:
                missing.append('templates/')
            print(f"FAIL: Component 1 — Missing: {', '.join(missing)}")
            # If basic structure doesn't exist, nothing else will work
            if not chart_yaml_exists and not values_yaml_exists and not templates_dir_exists:
                print(f"\nScore: {total_score}/1.0")
                print(f"REWARD: {total_score}")
                return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Required template files exist (0.15 points)
    # deployment.yaml, service.yaml, ingress.yaml, hpa.yaml, pdb.yaml
    try:
        required_templates = ['deployment.yaml', 'service.yaml', 'ingress.yaml', 'hpa.yaml', 'pdb.yaml']
        templates_path = os.path.join(WORKDIR, 'templates')
        found_templates = []
        missing_templates = []

        for tmpl in required_templates:
            if os.path.isfile(os.path.join(templates_path, tmpl)):
                found_templates.append(tmpl)
            else:
                missing_templates.append(tmpl)

        if len(found_templates) == len(required_templates):
            print(f"PASS: Component 2 — All 5 required template files exist (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Missing templates: {', '.join(missing_templates)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chart.yaml has correct metadata (0.10 points)
    # Must have name: myapp and apiVersion: v2
    try:
        with open(os.path.join(WORKDIR, 'Chart.yaml'), 'r') as f:
            chart_data = yaml.safe_load(f)

        name_ok = chart_data.get('name') == 'myapp'
        api_version_ok = chart_data.get('apiVersion') == 'v2'
        has_version = 'version' in chart_data

        if name_ok and api_version_ok and has_version:
            print(f"PASS: Component 3 — Chart.yaml has name=myapp, apiVersion=v2, version={chart_data.get('version')} (0.10 pts)")
            total_score += 0.10
        else:
            reasons = []
            if not name_ok:
                reasons.append(f"name={chart_data.get('name')}, expected myapp")
            if not api_version_ok:
                reasons.append(f"apiVersion={chart_data.get('apiVersion')}, expected v2")
            if not has_version:
                reasons.append("missing version field")
            print(f"FAIL: Component 3 — {'; '.join(reasons)}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 — Chart.yaml not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: values.yaml has required configuration sections (0.20 points)
    # Must include: replicaCount, image, service, ingress (with TLS), resources (with limits),
    # autoscaling, podDisruptionBudget
    try:
        with open(os.path.join(WORKDIR, 'values.yaml'), 'r') as f:
            values_data = yaml.safe_load(f)

        checks_passed = 0
        total_checks = 5

        # Check 4a: replicaCount and image section
        if 'replicaCount' in values_data and isinstance(values_data.get('image'), dict):
            img = values_data['image']
            if 'repository' in img and 'tag' in img:
                checks_passed += 1
                print(f"  Component 4a: replicaCount and image config present")
            else:
                print(f"  FAIL 4a: image missing repository or tag")
        else:
            print(f"  FAIL 4a: missing replicaCount or image section")

        # Check 4b: resources with limits
        resources = values_data.get('resources', {})
        if isinstance(resources, dict) and 'limits' in resources:
            limits = resources['limits']
            if 'cpu' in limits and 'memory' in limits:
                checks_passed += 1
                print(f"  Component 4b: resources.limits with cpu and memory present")
            else:
                print(f"  FAIL 4b: resources.limits missing cpu or memory")
        else:
            print(f"  FAIL 4b: missing resources.limits section")

        # Check 4c: ingress with TLS configuration
        ingress = values_data.get('ingress', {})
        if isinstance(ingress, dict) and 'enabled' in ingress and 'tls' in ingress:
            tls = ingress['tls']
            if isinstance(tls, list) and len(tls) > 0:
                checks_passed += 1
                print(f"  Component 4c: ingress with TLS configuration present")
            else:
                print(f"  FAIL 4c: ingress.tls is empty or not a list")
        else:
            print(f"  FAIL 4c: missing ingress.enabled or ingress.tls")

        # Check 4d: autoscaling (HPA) configuration
        autoscaling = values_data.get('autoscaling', {})
        if isinstance(autoscaling, dict) and 'enabled' in autoscaling and 'minReplicas' in autoscaling and 'maxReplicas' in autoscaling:
            checks_passed += 1
            print(f"  Component 4d: autoscaling configuration present")
        else:
            print(f"  FAIL 4d: missing or incomplete autoscaling section")

        # Check 4e: podDisruptionBudget configuration
        pdb = values_data.get('podDisruptionBudget', {})
        if isinstance(pdb, dict) and 'enabled' in pdb and ('minAvailable' in pdb or 'maxUnavailable' in pdb):
            checks_passed += 1
            print(f"  Component 4e: podDisruptionBudget configuration present")
        else:
            print(f"  FAIL 4e: missing or incomplete podDisruptionBudget section")

        comp4_score = 0.20 * (checks_passed / total_checks)
        if checks_passed == total_checks:
            print(f"PASS: Component 4 — All {total_checks} values.yaml config sections verified (0.20 pts)")
            total_score += 0.20
        elif checks_passed > 0:
            print(f"PARTIAL: Component 4 — {checks_passed}/{total_checks} config sections verified ({comp4_score:.2f} pts)")
            total_score += comp4_score
    except FileNotFoundError:
        print(f"FAIL: Component 4 — values.yaml not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: staging-values.yaml with correct overrides (0.20 points)
    # Must set replicaCount: 2 and ingress.enabled: true
    try:
        staging_path = None
        # Check common locations for staging values file
        for candidate in [
            os.path.join(WORKDIR, 'staging-values.yaml'),
            os.path.join(WORKDIR, 'staging_values.yaml'),
            os.path.join('/opt/helm', 'staging-values.yaml'),
            os.path.join('/home/user', 'staging-values.yaml'),
        ]:
            if os.path.isfile(candidate):
                staging_path = candidate
                break

        if staging_path is None:
            print(f"FAIL: Component 5 — staging-values.yaml not found in expected locations")
        else:
            with open(staging_path, 'r') as f:
                staging_data = yaml.safe_load(f)

            replica_ok = staging_data.get('replicaCount') == 2
            ingress_section = staging_data.get('ingress', {})
            ingress_enabled = (
                (isinstance(ingress_section, dict) and ingress_section.get('enabled') is True)
                or staging_data.get('ingress') is True  # flat override case
            )

            if replica_ok and ingress_enabled:
                print(f"PASS: Component 5 — staging-values.yaml has replicaCount=2 and ingress.enabled=true (0.20 pts)")
                total_score += 0.20
            else:
                reasons = []
                if not replica_ok:
                    reasons.append(f"replicaCount={staging_data.get('replicaCount')}, expected 2")
                if not ingress_enabled:
                    reasons.append(f"ingress.enabled not true (found: {ingress_section})")
                print(f"FAIL: Component 5 — {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Template files contain valid Helm templating and correct K8s resource kinds (0.20 points)
    try:
        templates_path = os.path.join(WORKDIR, 'templates')
        template_checks = {
            'deployment.yaml': {'kind': 'Deployment', 'helm_marker': '{{'},
            'service.yaml': {'kind': 'Service', 'helm_marker': '{{'},
            'ingress.yaml': {'kind': 'Ingress', 'helm_marker': '{{'},
            'hpa.yaml': {'kind': 'HorizontalPodAutoscaler', 'helm_marker': '{{'},
            'pdb.yaml': {'kind': 'PodDisruptionBudget', 'helm_marker': '{{'},
        }

        templates_ok = 0
        total_tmpl = len(template_checks)

        for tmpl_name, checks in template_checks.items():
            tmpl_path = os.path.join(templates_path, tmpl_name)
            if not os.path.isfile(tmpl_path):
                print(f"  FAIL 6-{tmpl_name}: file not found")
                continue

            with open(tmpl_path, 'r') as f:
                content = f.read()

            kind_found = f"kind: {checks['kind']}" in content
            helm_found = checks['helm_marker'] in content

            if kind_found and helm_found:
                templates_ok += 1
                print(f"  Component 6-{tmpl_name}: kind={checks['kind']}, has Helm templating")
            else:
                reasons = []
                if not kind_found:
                    reasons.append(f"missing kind: {checks['kind']}")
                if not helm_found:
                    reasons.append("no Helm templating found")
                print(f"  FAIL 6-{tmpl_name}: {'; '.join(reasons)}")

        comp6_score = 0.20 * (templates_ok / total_tmpl)
        if templates_ok == total_tmpl:
            print(f"PASS: Component 6 — All {total_tmpl} templates have correct kinds and Helm templating (0.20 pts)")
            total_score += 0.20
        elif templates_ok > 0:
            print(f"PARTIAL: Component 6 — {templates_ok}/{total_tmpl} templates validated ({comp6_score:.2f} pts)")
            total_score += comp6_score
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(WORKDIR):
    print(f"Directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task()
