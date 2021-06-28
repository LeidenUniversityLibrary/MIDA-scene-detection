BEGIN {
    start_ms = 0
    OFS = ","
    print "scene", "start_ms", "end_ms" }
/^frame/ {
    sub(/frame:/, "", $1)
    scene = $1
    sub(/pts:/, "", $2)
    end_ms = $2 # - 1
    print scene, start_ms, end_ms
    start_ms = $2
}
END {
    scene = scene + 1
    print scene, start_ms, -1
}