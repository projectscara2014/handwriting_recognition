all : 
	iverilog -o compiled.vvp vga_sync_signals_generator.v
	vvp compiled.vvp
	open simulation.vcd