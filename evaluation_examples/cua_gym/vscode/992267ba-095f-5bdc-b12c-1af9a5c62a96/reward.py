"""
Reward Script: Kubernetes deployment manifests and development workflow for Go API
Task ID: vscode_gf6_087
Domain: vscode
Scoring:
  - Component 1 (0.25): deployment.yaml with replicas, resources, probes, envFrom
  - Component 2 (0.10): service.yaml with ClusterIP, port 80->8080
  - Component 3 (0.10): configmap.yaml with app config data
  - Component 4 (0.10): kustomization.yaml listing base resources
  - Component 5 (0.15): dev overlay kustomization with 1-replica patch
  - Component 6 (0.15): Makefile k8s targets
  - Component 7 (0.15): .vscode/tasks.json with kubectl tasks
"""

import os
import json

try:
    import yaml
except ImportError:
    yaml = None

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-k8s-deploy')


def parse_yaml_simple(content):
    """Parse YAML content. Use PyYAML if available, else basic parsing."""
    if yaml is not None:
        return list(yaml.safe_load_all(content))
    # Fallback: return raw content for string-based checks
    return None


def read_file(path):
    """Read file content, return None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def verify_task():
    total_score = 0.0

    # Component 1: deployment.yaml (0.25 points)
    # Check: file exists, 2 replicas, resource requests/limits, liveness/readiness probes, envFrom
    try:
        dep_path = os.path.join(PROJECT, 'k8s', 'base', 'deployment.yaml')
        dep_content = read_file(dep_path)
        if dep_content is None:
            print("FAIL: Component 1 - deployment.yaml not found")
        else:
            comp1_score = 0.0
            docs = parse_yaml_simple(dep_content)

            if docs is not None and docs:
                doc = docs[0]
                spec = doc.get('spec', {})
                template_spec = spec.get('template', {}).get('spec', {})
                containers = template_spec.get('containers', [])
                container = containers[0] if containers else {}

                # 1a: replicas == 2
                if spec.get('replicas') == 2:
                    comp1_score += 0.05
                    print("PASS: Component 1a - replicas is 2")
                else:
                    print(f"FAIL: Component 1a - replicas is {spec.get('replicas')}, expected 2")

                # 1b: resource requests/limits
                resources = container.get('resources', {})
                req = resources.get('requests', {})
                lim = resources.get('limits', {})
                if (req.get('cpu') == '100m' and req.get('memory') == '128Mi' and
                        lim.get('cpu') == '500m' and lim.get('memory') == '256Mi'):
                    comp1_score += 0.05
                    print("PASS: Component 1b - resource requests/limits correct")
                else:
                    print(f"FAIL: Component 1b - resources: req={req}, lim={lim}")

                # 1c: liveness probe
                liveness = container.get('livenessProbe', {})
                liveness_http = liveness.get('httpGet', {})
                if (liveness_http.get('path') == '/health' and
                        liveness.get('initialDelaySeconds') == 30):
                    comp1_score += 0.05
                    print("PASS: Component 1c - liveness probe correct")
                else:
                    print(f"FAIL: Component 1c - liveness probe: {liveness}")

                # 1d: readiness probe
                readiness = container.get('readinessProbe', {})
                readiness_http = readiness.get('httpGet', {})
                if (readiness_http.get('path') == '/ready' and
                        readiness.get('initialDelaySeconds') == 10):
                    comp1_score += 0.05
                    print("PASS: Component 1d - readiness probe correct")
                else:
                    print(f"FAIL: Component 1d - readiness probe: {readiness}")

                # 1e: envFrom with configMapRef and secretRef
                env_from = container.get('envFrom', [])
                has_configmap_ref = any('configMapRef' in e for e in env_from)
                has_secret_ref = any('secretRef' in e for e in env_from)
                if has_configmap_ref and has_secret_ref:
                    comp1_score += 0.05
                    print("PASS: Component 1e - envFrom has configMapRef and secretRef")
                else:
                    print(f"FAIL: Component 1e - envFrom: configMapRef={has_configmap_ref}, secretRef={has_secret_ref}")

            else:
                # Fallback: string-based checks
                content_lower = dep_content.lower()
                if 'replicas: 2' in dep_content:
                    comp1_score += 0.05
                    print("PASS: Component 1a - replicas: 2 found (string)")
                else:
                    print("FAIL: Component 1a - replicas: 2 not found")

                if 'cpu: 100m' in dep_content and 'memory: 128Mi' in dep_content:
                    comp1_score += 0.05
                    print("PASS: Component 1b - resource requests found (string)")
                else:
                    print("FAIL: Component 1b - resource requests not found")

                if '/health' in dep_content and 'initialDelaySeconds: 30' in dep_content:
                    comp1_score += 0.05
                    print("PASS: Component 1c - liveness probe found (string)")
                else:
                    print("FAIL: Component 1c - liveness probe not found")

                if '/ready' in dep_content and 'initialDelaySeconds: 10' in dep_content:
                    comp1_score += 0.05
                    print("PASS: Component 1d - readiness probe found (string)")
                else:
                    print("FAIL: Component 1d - readiness probe not found")

                if 'configMapRef' in dep_content and 'secretRef' in dep_content:
                    comp1_score += 0.05
                    print("PASS: Component 1e - envFrom refs found (string)")
                else:
                    print("FAIL: Component 1e - envFrom refs not found")

            if comp1_score > 0:
                total_score += comp1_score
            print(f"  Component 1 subtotal: {comp1_score}/0.25")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: service.yaml (0.10 points)
    try:
        svc_path = os.path.join(PROJECT, 'k8s', 'base', 'service.yaml')
        svc_content = read_file(svc_path)
        if svc_content is None:
            print("FAIL: Component 2 - service.yaml not found")
        else:
            docs = parse_yaml_simple(svc_content)
            if docs is not None and docs:
                doc = docs[0]
                svc_spec = doc.get('spec', {})
                svc_type = svc_spec.get('type', '')
                ports = svc_spec.get('ports', [])
                port_ok = any(p.get('port') == 80 and p.get('targetPort') == 8080 for p in ports)
                if svc_type == 'ClusterIP' and port_ok:
                    total_score += 0.10
                    print("PASS: Component 2 - service.yaml: ClusterIP, port 80->8080 (0.10 pts)")
                else:
                    print(f"FAIL: Component 2 - type={svc_type}, port_ok={port_ok}")
            else:
                # String fallback
                if 'ClusterIP' in svc_content and 'port: 80' in svc_content and 'targetPort: 8080' in svc_content:
                    total_score += 0.10
                    print("PASS: Component 2 - service.yaml correct (string) (0.10 pts)")
                else:
                    print("FAIL: Component 2 - service.yaml missing expected values")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: configmap.yaml (0.10 points)
    try:
        cm_path = os.path.join(PROJECT, 'k8s', 'base', 'configmap.yaml')
        cm_content = read_file(cm_path)
        if cm_content is None:
            print("FAIL: Component 3 - configmap.yaml not found")
        else:
            docs = parse_yaml_simple(cm_content)
            if docs is not None and docs:
                doc = docs[0]
                kind = doc.get('kind', '')
                data = doc.get('data', {})
                if kind == 'ConfigMap' and len(data) > 0:
                    total_score += 0.10
                    print(f"PASS: Component 3 - configmap.yaml: kind=ConfigMap, {len(data)} data keys (0.10 pts)")
                else:
                    print(f"FAIL: Component 3 - kind={kind}, data keys={len(data)}")
            else:
                if 'kind: ConfigMap' in cm_content and 'data:' in cm_content:
                    total_score += 0.10
                    print("PASS: Component 3 - configmap.yaml correct (string) (0.10 pts)")
                else:
                    print("FAIL: Component 3 - configmap.yaml missing expected values")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: kustomization.yaml base (0.10 points)
    try:
        kust_path = os.path.join(PROJECT, 'k8s', 'base', 'kustomization.yaml')
        kust_content = read_file(kust_path)
        if kust_content is None:
            print("FAIL: Component 4 - base kustomization.yaml not found")
        else:
            docs = parse_yaml_simple(kust_content)
            if docs is not None and docs:
                doc = docs[0]
                resources = doc.get('resources', [])
                has_deployment = any('deployment' in str(r).lower() for r in resources)
                has_service = any('service' in str(r).lower() for r in resources)
                has_configmap = any('configmap' in str(r).lower() for r in resources)
                if has_deployment and has_service and has_configmap:
                    total_score += 0.10
                    print(f"PASS: Component 4 - base kustomization lists all resources (0.10 pts)")
                else:
                    print(f"FAIL: Component 4 - resources: dep={has_deployment}, svc={has_service}, cm={has_configmap}")
            else:
                if ('deployment.yaml' in kust_content and 'service.yaml' in kust_content
                        and 'configmap.yaml' in kust_content):
                    total_score += 0.10
                    print("PASS: Component 4 - base kustomization correct (string) (0.10 pts)")
                else:
                    print("FAIL: Component 4 - base kustomization missing resources")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: dev overlay kustomization (0.15 points)
    try:
        dev_path = os.path.join(PROJECT, 'k8s', 'overlays', 'dev', 'kustomization.yaml')
        dev_content = read_file(dev_path)
        if dev_content is None:
            print("FAIL: Component 5 - dev kustomization.yaml not found")
        else:
            comp5_score = 0.0
            # Check references base
            if '../../base' in dev_content or '../base' in dev_content:
                comp5_score += 0.05
                print("PASS: Component 5a - dev overlay references base")
            else:
                print("FAIL: Component 5a - dev overlay does not reference base")

            # Check patches for 1 replica
            if 'replica' in dev_content.lower() and '1' in dev_content:
                comp5_score += 0.05
                print("PASS: Component 5b - dev overlay patches replicas to 1")
            else:
                print("FAIL: Component 5b - dev overlay missing replica patch")

            # Check dev-specific env vars
            if 'dev' in dev_content.lower() or 'debug' in dev_content.lower():
                comp5_score += 0.05
                print("PASS: Component 5c - dev overlay has dev-specific env vars")
            else:
                print("FAIL: Component 5c - dev overlay missing dev-specific env vars")

            if comp5_score > 0:
                total_score += comp5_score
            print(f"  Component 5 subtotal: {comp5_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Makefile k8s targets (0.15 points)
    try:
        makefile_path = os.path.join(PROJECT, 'Makefile')
        makefile_content = read_file(makefile_path)
        if makefile_content is None:
            print("FAIL: Component 6 - Makefile not found")
        else:
            comp6_score = 0.0
            if 'k8s-apply' in makefile_content and 'kubectl' in makefile_content:
                comp6_score += 0.05
                print("PASS: Component 6a - Makefile has k8s-apply target")
            else:
                print("FAIL: Component 6a - Makefile missing k8s-apply target")

            if 'k8s-delete' in makefile_content:
                comp6_score += 0.05
                print("PASS: Component 6b - Makefile has k8s-delete target")
            else:
                print("FAIL: Component 6b - Makefile missing k8s-delete target")

            if 'k8s-status' in makefile_content:
                comp6_score += 0.05
                print("PASS: Component 6c - Makefile has k8s-status target")
            else:
                print("FAIL: Component 6c - Makefile missing k8s-status target")

            if comp6_score > 0:
                total_score += comp6_score
            print(f"  Component 6 subtotal: {comp6_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: .vscode/tasks.json with kubectl tasks (0.15 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        tasks_content = read_file(tasks_path)
        if tasks_content is None:
            print("FAIL: Component 7 - .vscode/tasks.json not found")
        else:
            tasks_json = json.loads(tasks_content)
            task_labels = [t.get('label', '') for t in tasks_json.get('tasks', [])]
            task_commands = [t.get('command', '') for t in tasks_json.get('tasks', [])]
            all_commands = ' '.join(task_commands)

            comp7_score = 0.0
            # Must have kubectl-related tasks
            has_kubectl_tasks = 'kubectl' in all_commands
            has_k8s_labels = any('k8s' in label.lower() or 'kube' in label.lower() for label in task_labels)

            if has_kubectl_tasks and has_k8s_labels:
                comp7_score += 0.10
                print(f"PASS: Component 7a - tasks.json has kubectl tasks with k8s labels (0.10 pts)")
            elif has_kubectl_tasks:
                comp7_score += 0.05
                print(f"PARTIAL: Component 7a - tasks.json has kubectl but labels don't match")
            else:
                print(f"FAIL: Component 7a - tasks.json missing kubectl tasks")

            # At least 3 tasks
            if len(tasks_json.get('tasks', [])) >= 3:
                comp7_score += 0.05
                print(f"PASS: Component 7b - tasks.json has {len(tasks_json.get('tasks', []))} tasks (>=3) (0.05 pts)")
            else:
                print(f"FAIL: Component 7b - tasks.json has {len(tasks_json.get('tasks', []))} tasks, expected >=3")

            if comp7_score > 0:
                total_score += comp7_score
            print(f"  Component 7 subtotal: {comp7_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
