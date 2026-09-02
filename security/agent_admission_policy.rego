package pipefish.admission

# Deny any container running as root
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.runAsNonRoot
    msg := sprintf("Container '%v' in pod '%v' must set securityContext.runAsNonRoot = true", [container.name, input.request.object.metadata.name])
}

# Deny containers without readOnlyRootFilesystem
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.readOnlyRootFilesystem != true
    msg := sprintf("Container '%v' in pod '%v' must set securityContext.readOnlyRootFilesystem = true", [container.name, input.request.object.metadata.name])
}

# Deny hostPath mounts (prevents container breakout to host filesystem)
deny[msg] {
    input.request.kind.kind == "Pod"
    volume := input.request.object.spec.volumes[_]
    volume.hostPath
    msg := sprintf("Pod '%v' is prohibited from using hostPath volumes (Zero-Trust Policy)", [input.request.object.metadata.name])
}

# Require CPU & memory resource limits
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.cpu
    msg := sprintf("Container '%v' in pod '%v' must define CPU limits", [container.name, input.request.object.metadata.name])
}
