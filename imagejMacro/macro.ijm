function action(input, output, filename) {
	open(input + filename);
	run("Set Scale...", "distance=2048 known=5000 unit=nm");
	setOption("BlackBackground", false);
	run("Convert to Mask");
	run("Analyze Particles...", "size=500.00-Infinity circularity=0.05-1.00 display exclude clear summarize add");
	run("Distribution...", "parameter=Area automatic");
	saveAs("Jpeg", output + filename);
	close();
	selectWindow(filename);
	close();
}

input = "D:/dev/ebl/test/SIMDATA/R38/";
output2 = "D:/dev/ebl/test/imagej/Simulation/R38/";

list = getFileList(input);
for (i = 0; i < list.length; i++) {
	action(input, output2, list[i]);
}
