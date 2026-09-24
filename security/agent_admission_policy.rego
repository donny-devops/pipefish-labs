package pipefish.admission

import rego.v1

# Deny any container running as root
deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.runAsNonRoot
    msg := sprintf("Container '%v' in pod '%v' must set securityContext.runAsNonRoot = true", [container.name, input.request.object.metadata.name])
}

# Deny containers running in privileged mode
deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged == true
    msg := sprintf("Container '%v' in pod '%v' cannot run in privileged mode (Zero-Trust Policy)", [container.name, input.request.object.metadata.name])
}

# Deny containers with privilege escalation allowed
deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.allowPrivilegeEscalation != false
    msg := sprintf("Container '%v' in pod '%v' must explicitly set allowPrivilegeEscalation = false", [container.name, input.request.object.metadata.name])
}

# Deny containers without readOnlyRootFilesystem
deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.readOnlyRootFilesystem != true
    msg := sprintf("Container '%v' in pod '%v' must set securityContext.readOnlyRootFilesystem = true", [container.name, input.request.object.metadata.name])
}

# Deny hostPath mounts (prevents container breakout to host filesystem)
deny contains msg if {
    input.request.kind.kind == "Pod"
    volume := input.request.object.spec.volumes[_]
    volume.hostPath
    msg := sprintf("Pod '%v' is prohibited from using hostPath volumes (Zero-Trust Policy)", [input.request.object.metadata.name])
}

# Deny sharing host namespaces (hostNetwork, hostPID, hostIPC)
deny contains msg if {
    input.request.kind.kind == "Pod"
    input.request.object.spec.hostNetwork == true
    msg := sprintf("Pod '%v' is prohibited from sharing hostNetwork", [input.request.object.metadata.name])
}

deny contains msg if {
    input.request.kind.kind == "Pod"
    input.request.object.spec.hostPID == true
    msg := sprintf("Pod '%v' is prohibited from sharing hostPID", [input.request.object.metadata.name])
}

deny contains msg if {
    input.request.kind.kind == "Pod"
    input.request.object.spec.hostIPC == true
    msg := sprintf("Pod '%v' is prohibited from sharing hostIPC", [input.request.object.metadata.name])
}

# Require CPU & memory resource limits
deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.cpu
    msg := sprintf("Container '%v' in pod '%v' must define CPU limits", [container.name, input.request.object.metadata.name])
}

deny contains msg if {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.memory
    msg := sprintf("Container '%v' in pod '%v' must define memory limits", [container.name, input.request.object.metadata.name])
}
