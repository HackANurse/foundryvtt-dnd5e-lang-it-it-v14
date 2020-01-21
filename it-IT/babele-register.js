
Hooks.on('init', () => {

	if(typeof Babele !== 'undefined') {
		
		Babele.get().register({
			module: 'FoundryVTT-dnd5e-it',
			lang: 'it',
			dir: 'compendium'
		});

		Babele.get().registerConverters({
			"weight": (value) => { return parseInt(value)/2 },
			"range": (range) => { 
				if(range.units === 'ft') {
					return mergeObject(range, { value: range.value*0.3 });	
				} 
				if(range.units === 'mi') {
					return mergeObject(range, { value: range.value*1.5 });	
				}
				return range;	
				
			}
		});
	}
	
});