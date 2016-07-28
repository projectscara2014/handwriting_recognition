WORKING_DIRECTORY = /Users/ironstein/Documents/projects_working_directory/handwriting_recognition/FPGA/final_working_projects/uart_core
all : 
	iverilog -o compiled.vvp -I $(WORKING_DIRECTORY)/uart_rx_core -I $(WORKING_DIRECTORY)/uart_tx_core -I $(WORKING_DIRECTORY)/uart_rx_core/utils -I $(WORKING_DIRECTORY)/uart_tx_core/utils uart_core.v
	vvp compiled.vvp
	open simulation.vcd