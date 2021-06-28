BEGIN { FS = "," }
/^[0-9]/ {
    scene = sprintf( "%0.4d", $1 )
    time_in = $2
    time_out = $3
    printf "mkdir -p data_out/scene-%s\n", scene
    printf "ffmpeg -report -ss %dms -to %dms ", time_in, time_out
    printf "-i data/%s -vsync 2 data_out/scene-%s/frame-%%03d.jpg\n", video, scene
    # printf "ffmpeg -report -ss %dms -to %dms -i data/%s -vsync 2 data_out/scene-%s/frame-%%03d.jpg", time_in, time_out, video, scene
}