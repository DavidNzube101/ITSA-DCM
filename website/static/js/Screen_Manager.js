console.log(`[INFO]: Loaded page to screen ${current_screen}`)

// ScreenElement, ScreenID 

home_screen = [document.querySelector("#SCM-HOME-SCREEN"), 1]
technicians_screen = [document.querySelector("#SCM-TECHNICIANS-SCREEN"), 2]
organization_screen = [document.querySelector("#SCM-ORGANIZATIONS-SCREEN"), 3]
device_screen = [document.querySelector("#SCM-DEVICE-SCREEN"), 4]
requests_screen = [document.querySelector("#SCM-REQUESTS-SCREEN"), 5]
manage_screen = [document.querySelector("#SCM-MANAGE-STAFFS-SCREEN"), 6]

// Trigger's
home_trigger = document.querySelector("#SCM-HOME")
technicians_trigger = document.querySelector("#SCM-TECHNICIANS")
organization_trigger = document.querySelector("#SCM-ORGANIZATION")
device_trigger = document.querySelector("#SCM-DEVICE")
requests_trigger = document.querySelector("#SCM-REQUESTS")
manage_trigger = document.querySelector("#SCM-MANAGE-STAFFS")
// merchant_trigger = document.querySelector("#merchant-trigger")

window.addEventListener('load', ()=>{
	// window.location.href = `/dashboard/${current_screen}`
	switch (current_screen) {
	
		case 2:
			home_screen[0].style.display = 'none'
			organization_screen[0].style.display = 'none'
			technicians_screen[0].style.display = 'grid'
			technicians_screen[0].className = 'active-screen screens'
			technicians_trigger.className = 'active-page-trigger'
			device_screen[0].style.display = 'none'
			requests_screen[0].style.display = 'none'
			manage_screen[0].style.display = 'none'
			current_screen = 2
			break;

		case 3:
			home_screen[0].style.display = 'none'
			organization_screen[0].style.display = 'grid'
			organization_screen[0].className = 'active-screen screens'
			organization_trigger.className = 'active-page-trigger'
			technicians_screen[0].style.display = 'none'
			device_screen[0].style.display = 'none'
			requests_screen[0].style.display = 'none'
			manage_screen[0].style.display = 'none'
			current_screen = 3
			break;

		case 4:
			home_screen[0].style.display = 'none'
			organization_screen[0].style.display = 'none'
			device_screen[0].style.display = 'grid'
			device_screen[0].className = 'active-screen screens'
			device_trigger.className = 'active-page-trigger'
			technicians_screen[0].style.display = 'none'
			requests_screen[0].style.display = 'none'
			manage_screen[0].style.display = 'none'
			current_screen = 4
			break;

		case 5:
			home_screen[0].style.display = 'none'
			requests_screen[0].style.display = 'grid'
			requests_screen[0].className = 'active-screen screens'
			requests_trigger.className = 'active-page-trigger'
			organization_screen[0].style.display = 'none'
			technicians_screen[0].style.display = 'none'
			device_screen[0].style.display = 'none'
			manage_screen[0].style.display = 'none'
			current_screen = 5
			break;

		case 6:
			home_screen[0].style.display = 'none'
			manage_screen[0].style.display = 'grid'
			manage_screen[0].className = 'active-screen screens'
			manage_trigger.className = 'active-page-trigger'
			organization_screen[0].style.display = 'none'
			technicians_screen[0].style.display = 'none'
			device_screen[0].style.display = 'none'
			requests_screen[0].style.display = 'none'
			current_screen = 6
			break;


		default:
			home_screen[0].style.display = 'grid'
			home_screen[0].className = 'active-screen screens'
			organization_screen[0].style.display = 'none'
			home_trigger.className = 'active-page-trigger'
			technicians_screen[0].style.display = 'none'
			device_screen[0].style.display = 'none'
			requests_screen[0].style.display = 'none'
			manage_screen[0].style.display = 'none'
	}

})

home_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'grid'
	home_screen[0].className = "active-screen"
	home_trigger.className = 'active-page-trigger'
	organization_screen[0].style.display = 'none'
	technicians_screen[0].style.display = 'none'	
	
	organization_trigger.className = ''
	technicians_trigger.className = ''

	device_trigger.className = ''
	device_screen[0].style.display = 'none'
	requests_trigger.className = ''
	requests_screen[0].style.display = 'none'
	manage_trigger.className = ''
	manage_screen[0].style.display = 'none'

	current_screen = 1
})
technicians_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	organization_screen[0].style.display = 'none'
	technicians_screen[0].style.display = 'grid'
	technicians_screen[0].className = 'active-screen screens'
	technicians_trigger.className = 'active-page-trigger'

	device_trigger.className = ''
	device_screen[0].style.display = 'none'
	requests_trigger.className = ''
	requests_screen[0].style.display = 'none'
	manage_trigger.className = ''
	manage_screen[0].style.display = 'none'

	organization_trigger.className = ''
	home_trigger.className = ''

	current_screen = 2
})
organization_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	organization_screen[0].style.display = 'grid'
	organization_screen[0].className = 'active-screen screens'
	organization_trigger.className = 'active-page-trigger'

	device_trigger.className = ''
	device_screen[0].style.display = 'none'
	requests_trigger.className = ''
	requests_screen[0].style.display = 'none'
	manage_trigger.className = ''
	manage_screen[0].style.display = 'none'

	home_trigger.className = ''
	technicians_trigger.className = ''

	technicians_screen[0].style.display = 'none'
	current_screen = 3
})
device_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'

	device_screen[0].style.display = 'grid'
	device_screen[0].className = 'active-screen screens'
	device_trigger.className = 'active-page-trigger'

	home_trigger.className = ''
	technicians_trigger.className = ''

	technicians_screen[0].style.display = 'none'

	requests_trigger.className = ''
	requests_screen[0].style.display = 'none'
	manage_trigger.className = ''
	manage_screen[0].style.display = 'none'
	current_screen = 4
})
requests_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	requests_screen[0].style.display = 'grid'
	requests_screen[0].className = 'active-screen screens'
	requests_trigger.className = 'active-page-trigger'

	device_trigger.className = ''
	device_screen[0].style.display = 'none'
	manage_trigger.className = ''
	manage_screen[0].style.display = 'none'

	home_trigger.className = ''
	technicians_trigger.className = ''

	technicians_screen[0].style.display = 'none'
	current_screen = 5
})
manage_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	manage_screen[0].style.display = 'grid'
	manage_screen[0].className = 'active-screen screens'
	manage_trigger.className = 'active-page-trigger'

	device_trigger.className = ''
	device_screen[0].style.display = 'none'
	requests_trigger.className = ''
	requests_screen[0].style.display = 'none'

	home_trigger.className = ''
	technicians_trigger.className = ''

	technicians_screen[0].style.display = 'none'
	current_screen = 6
})
