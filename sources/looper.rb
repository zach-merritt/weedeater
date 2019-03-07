slave = IO.popen(['python3', './predict_plant_02.py', '../models/first_model.h5', 'current_image.jpg'],mode='r+')
sleep(4)
(0..2).each do
  puts "in loop, about to send"
  slave.write "current_image.jpg\n"
  slave.flush
  slave.flush
  puts "sent"
  #slave.close_write
  line = slave.readline
  while line do
    sleep 2
    puts line
    slave.write "current_image.jpg\n"
    slave.flush
    break if slave.eof
    line = slave.readline
  end
end
