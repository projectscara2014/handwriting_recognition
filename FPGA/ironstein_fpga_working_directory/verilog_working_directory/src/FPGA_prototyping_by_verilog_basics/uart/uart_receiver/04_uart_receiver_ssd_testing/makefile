WORKING_DIRECTORY=/Users/ironstein/Documents/projects_working_directory/handwriting_recognition/FPGA/ironstein_fpga_working_directory/verilog_working_directory/src/FPGA_prototyping_by_verilog_basics/uart/uart_receiver/04_uart_receiver_ssd_testing
all :
	iverilog -o compiled.vvp \
	-I $(WORKING_DIRECTORY)/integer_seven_segment_display_controller/seven_segment_display_core/utils \
	-I $(WORKING_DIRECTORY)/reset_controller \
	-I $(WORKING_DIRECTORY)/integer_seven_segment_display_controller/seven_segement_display_core \
	-I $(WORKING_DIRECTORY)/integer_seven_segment_display_controller/binary_to_bcd_core \
	-I $(WORKING_DIRECTORY)/uart_rx_core \
	-I $(WORKING_DIRECTORY)/integer_seven_segment_display_controller \
	uart_receiver_ssd_test.v