"""
Reward Script: GitOps-style systemd path unit deployment
Task ID: os_gff_051
Domain: libreoffice_calc (actually OS/systemd)
Scoring:
  Component 1: gitops-watch.path file exists with correct PathModified directive (0.25)
  Component 2: gitops-apply.service file exists with correct ExecStart kubectl command (0.25)
  Component 3: Both units are enabled (symlinked in multi-user.target.wants) (0.20)
  Component 4: Path unit is active (waiting) via D-Bus (0.15)
  Component 5: Service unit references correct Unit in path and correct Type in service (0.15)
"""

import os
import re


def verify_task():
    """
    Verify systemd GitOps deployment with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    PATH_UNIT = '/etc/systemd/system/gitops-watch.path'
    SERVICE_UNIT = '/etc/systemd/system/gitops-apply.service'
    ENABLED_PATH_LINK = '/etc/systemd/system/multi-user.target.wants/gitops-watch.path'
    ENABLED_SVC_LINK = '/etc/systemd/system/multi-user.target.wants/gitops-apply.service'

    # Component 1: gitops-watch.path exists with PathModified=/opt/deploy/manifests (0.25 points)
    try:
        if os.path.isfile(PATH_UNIT):
            with open(PATH_UNIT, 'r') as f:
                path_content = f.read()
            # Must contain PathModified pointing to /opt/deploy/manifests
            if re.search(r'PathModified\s*=\s*/opt/deploy/manifests', path_content):
                print(f"PASS: Component 1 -- gitops-watch.path exists with PathModified=/opt/deploy/manifests (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- gitops-watch.path exists but missing PathModified=/opt/deploy/manifests")
                print(f"  Content: {path_content[:200]}")
        else:
            print(f"FAIL: Component 1 -- {PATH_UNIT} does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: gitops-apply.service exists with ExecStart running kubectl apply (0.25 points)
    try:
        if os.path.isfile(SERVICE_UNIT):
            with open(SERVICE_UNIT, 'r') as f:
                svc_content = f.read()
            # Must contain ExecStart with kubectl apply -f /opt/deploy/manifests/
            if re.search(r'ExecStart\s*=.*kubectl\s+apply\s+-f\s+/opt/deploy/manifests', svc_content):
                print(f"PASS: Component 2 -- gitops-apply.service exists with correct ExecStart (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- gitops-apply.service exists but ExecStart does not match expected pattern")
                print(f"  Content: {svc_content[:200]}")
        else:
            print(f"FAIL: Component 2 -- {SERVICE_UNIT} does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Both units are enabled (symlinks in multi-user.target.wants) (0.20 points)
    try:
        path_enabled = os.path.exists(ENABLED_PATH_LINK)
        svc_enabled = os.path.exists(ENABLED_SVC_LINK)
        if path_enabled and svc_enabled:
            print(f"PASS: Component 3 -- Both units enabled (symlinks exist in multi-user.target.wants) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- path enabled={path_enabled}, service enabled={svc_enabled}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Path unit is active (waiting) via D-Bus (0.15 points)
    try:
        import dbus
        bus = dbus.SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')
        unit_path = manager.GetUnit('gitops-watch.path')
        unit_obj = bus.get_object('org.freedesktop.systemd1', str(unit_path))
        props = dbus.Interface(unit_obj, 'org.freedesktop.DBus.Properties')
        active_state = str(props.Get('org.freedesktop.systemd1.Unit', 'ActiveState'))
        if active_state == 'active':
            print(f"PASS: Component 4 -- gitops-watch.path is active (waiting) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- gitops-watch.path ActiveState={active_state}, expected 'active'")
    except Exception as e:
        print(f"FAIL: Component 4 -- Cannot query unit active state: {e}")

    # Component 5: Path unit references gitops-apply.service AND service Type=oneshot (0.15 points)
    try:
        path_refs_svc = (
            os.path.isfile(PATH_UNIT)
            and re.search(r'Unit\s*=\s*gitops-apply\.service', open(PATH_UNIT).read()) is not None
        )
        svc_is_oneshot = (
            os.path.isfile(SERVICE_UNIT)
            and re.search(r'Type\s*=\s*oneshot', open(SERVICE_UNIT).read()) is not None
        )

        if path_refs_svc and svc_is_oneshot:
            print(f"PASS: Component 5 -- Path unit targets gitops-apply.service AND service Type=oneshot (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- path references service={path_refs_svc}, service type=oneshot={svc_is_oneshot}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
