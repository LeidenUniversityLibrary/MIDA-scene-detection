BEGIN { FS = "," }
/^[0-9]/ {
    scene = sprintf( "%0.4d", $1 )
    time_in = $2
    time_out = $3
    printf "mkdir -p data_out/scene-%s\n", scene
    printf "ffmpeg -report -ss %s -to %s ", time_in, time_out
    printf "-i data/%s -copyts -frame_pts true data_out/scene-%s/frame-%%d.jpg\n", video, scene
}