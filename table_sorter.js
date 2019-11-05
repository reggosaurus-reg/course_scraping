// This file contains the table sorting behaviour for the Course web page

alert("This is the table sorter speaking!")

window.onload = () => {
	document.querySelectorAll("th").forEach((o) => { 
		o.onclick = function() {
			currently_sorted = document.getElementById("sorting");
			// Nothing is marked for sorting
			if (currently_sorted == null) {
				o.setAttribute("id", "sorting");
				o.classList.add("ascending");
			}
			// Some other element is marked
			else if (currently_sorted != o) {
				currently_sorted.removeAttribute("id");
				currently_sorted.removeAttribute("class");
				o.setAttribute("id", "sorting");
				o.classList.add("ascending");
			}
			// This element is marked
			else {
				// Won't circle (here). ascending -> descending -> unmark
				if (o.classList.contains("ascending")) {
					o.classList.remove("ascending");
					o.classList.add("descending");
				}
				else if (o.classList.contains("descending")) {
					o.classList.remove("descending");
					currently_sorted.removeAttribute("id");
					currently_sorted.removeAttribute("class");
				}
			}
		};
	});
};
