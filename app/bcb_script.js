
nvvindilnk = new Array();
for(u=1; u<=4; u++){
	nvvindilnk[u] = new Array();
	for(v=1; v<=10; v++){
		nvvindilnk[u][v] = new Array();
		for(w=1; w<=10; w++){
			nvvindilnk[u][v][w] = "";
		}
	}
}
// TAB 1
//nvvindilnk[1][2][1] = "dolar/bolsin.php";
//nvvindilnk[1][2][2] = "dolar/bolsin_hist.php";
//nvvindilnk[1][2][3] = "dolar/periodos.php";
//nvvindilnk[1][2][4] = "dolar/anual.php";
// nvvindilnk[1][2][4] = "../../index.php?q=indicadores/_lista&ic=14&ids=1&zplane=2";
//-------------------------------------
//nvvindilnk[1][2][5] = "dolar/tabla.php?moneda=34&range=USD";
//nvvindilnk[1][3][1] = "euro/ultimo.php";
//nvvindilnk[1][3][2] = "euro/anteriores.php";
//nvvindilnk[1][1][1] = "otras/ultimo.php";
//nvvindilnk[1][1][2] = "otras/anteriores.php";
//nvvindilnk[1][4][1] = "deg/ultimo.php";
//nvvindilnk[1][4][2] = "deg/anteriores.php";
nvvindilnk[1][5][1] = "ufv/ultimo.php";
nvvindilnk[1][5][2] = "ufv/otros.php";
//nvvindilnk[1][5][3] = "ufv/evolucion.php";
//nvvindilnk[1][5][3] = "../../index.php?q=indicadores/_lista&ic=3&ids=13&zplane=2";
nvvindilnk[1][5][3] = "ufv/anual.001.php";

//------------------------------------
nvvindilnk[1][5][4] = "ufv/gestion.php";
//nvvindilnk[1][6][1] = "metales/ultimo.php";
//nvvindilnk[1][6][2] = "metales/anteriores.php";
//nvvindilnk[1][7][1] = "libor/ultimo.php";
//nvvindilnk[1][7][2] = "libor/anteriores.php";
//nvvindilnk[1][8][1] = "../../index.php?q=indicadores/_lista&ic=4&zplane=2";
//nvvindilnk[1][8][2] = "../../index.php?q=indicadores/_lista&ic=4&zplane=2";
//nvvindilnk[1][9][1] = "../../index.php?q=indicadores/_lista&ic=16&zplane=2";
//---------------------------------------------------------

// TAB 4
//nvvindilnk[4][1][1] = "inflacion/ultimo.php";
//nvvindilnk[4][1][2] = "inflacion/anteriores.php";

// combos reset
function nvf_resetcombosBox1(){
	nvjs_indiLoadF(1,5,1);
	document.forms["indibox1"]["subcateg1"].selectedIndex = 0;
	document.forms["indibox1"]["combos1_5"].selectedIndex = 0;
	nvjs_indiChanger(0);
	document.getElementById('subcateg1_data1').style.display = 'block';
	subcateg_o = 1;
}
function nvf_resetcombosBox4(){
	nvjs_indiLoadF(1,5,1);
	document.forms["indibox4"]["combos1_5"].selectedIndex = 0;
}
// combos changer
subcateg_o = 1;
function nvjs_indiChanger(subcateg){
	// TAB 1 only
	subcateg++;
	document.getElementById('subcateg1_data'+subcateg).style.display = 'none';
	document.getElementById('subcateg1_data'+subcateg_o).style.display = 'block';
	subcateg_o = subcateg;
}
function nvjs_indiLoad(nvvn1,nvvn2){
	//alert (document.forms["indibox"+nvvn1]["subcateg1"].value);
	if (document.forms["indibox"+nvvn1]["subcateg1"].value == 7)
	{
		location.href="?q=compvenmonext";
	}
	else
	{		
		if (document.forms["indibox"+nvvn1]["combos"+nvvn1+"_"+nvvn2]!=null){
			nvvn3 = document.forms["indibox"+nvvn1]["combos"+nvvn1+"_"+nvvn2].selectedIndex+1;
		}else{
			nvv3 = 1;
		}
		frames["indiframe"].location.href = "librerias/indicadores/"+nvvindilnk[nvvn1][nvvn2][nvvn3];
	}
}
// load pages into iframe
function nvjs_indiLoadF(nvvn1,nvvn2,nvvn3){
	frames["indiframe"].location.href = "librerias/indicadores/"+nvvindilnk[nvvn1][nvvn2][nvvn3];
}
// TAB buttons changer
nvv_indiBox2Actual = 1;
function nvjs_indiBox2(cual){
	if (cual!=nvv_indiBox2Actual){
		document.getElementById('nvo_indibox2_'+nvv_indiBox2Actual).style.display = 'none';
		document.getElementById('nvo_indibox2_'+cual).style.display = 'block';
		document.getElementById('nvo_indibox2lnk'+nvv_indiBox2Actual).className = 'nvdec-box2tab';
		document.getElementById('nvo_indibox2lnk'+cual).className = 'nvdec-box2tabsel';
		switch(cual){
			case 1: nvf_resetcombosBox1();
					break;
			case 2: nvf_load_ajax('librerias/indicadores/pdf/lista.php',6)
					break;
			case 3: nvf_load_ajax('librerias/indicadores/pdf/lista.php',7)
					break;
			case 4: nvf_resetcombosBox4();
					break;
		}
		nvv_indiBox2Actual = cual;
	}
}
//lamada al ajax
function nvf_load_ajax(url,idc){
	switch (idc) {
		case 6:	tm=2;a=3;break;
		case 7: tm=3;a=2;break;
	}
	//descargar la pagina previa
	//$('#nvo_indibox2_'+a).load('vacio.php');
	document.getElementById('nvo_indibox2_'+a).innerHTML='';
	//cargar la nueva pagina
	$('#nvo_indibox2_'+tm).load(url+'?idc='+idc);
	var di=document.getElementById('nvo_indibox2_'+tm);
	di.style.display = 'block';
}
