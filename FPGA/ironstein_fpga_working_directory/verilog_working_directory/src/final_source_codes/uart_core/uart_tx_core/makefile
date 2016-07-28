WORKING_DIRECTORY = /Users/ironstein/Documents/projects_working_directory/handwriting_recognition/FPGA/ironstein_fpga_working_directory/verilog_working_directory/src/final_source_codes/uart_core/uart_tx_core
all : 
	iverilog -o compiled.vvp \
	-I $(WORKING_DIRECTORY)/utils \
	uart_tx_core.v

	vvp compiled.vvp