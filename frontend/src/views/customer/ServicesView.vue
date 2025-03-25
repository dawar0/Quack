import { ref, computed } from "vue"; import { useRouter } from "vue-router"; import { NeoButton,
NeoCard, NeoInput, NeoSelect, NeoModal, NeoBadge, } from "@/components/ui"; const router =
useRouter(); // Sample services data - in a real app, this would come from an API const services =
ref([ { id: 1, name: "House Cleaning", price: 75, time_required: "2 hours", description: "Complete
house cleaning service including dusting, mopping, and bathroom cleaning.", image:
"https://placehold.co/600x400?text=House+Cleaning", features: ["Dusting", "Mopping", "Bathroom
Cleaning", "Kitchen Cleaning"], }, { id: 2, name: "Plumbing", price: 120, time_required: "1-3
hours", description: "Professional plumbing services for repairs, installations, and maintenance.",
image: "https://placehold.co/600x400?text=Plumbing", features: [ "Leak Repair", "Pipe Installation",
"Drain Cleaning", "Fixture Installation", ], }, { id: 3, name: "Electrical Work", price: 150,
time_required: "2-4 hours", description: "Licensed electricians for all your electrical needs, from
repairs to installations.", image: "https://placehold.co/600x400?text=Electrical", features: [
"Wiring", "Light Fixtures", "Outlet Installation", "Electrical Panel Upgrades", ], }, { id: 4, name:
"Gardening", price: 90, time_required: "3 hours", description: "Complete garden maintenance
including mowing, trimming, and planting.", image: "https://placehold.co/600x400?text=Gardening",
features: ["Mowing", "Trimming", "Planting", "Weeding"], }, { id: 5, name: "Painting", price: 200,
time_required: "5-8 hours", description: "Professional painting services for interior and exterior
surfaces.", image: "https://placehold.co/600x400?text=Painting", features: [ "Interior Painting",
"Exterior Painting", "Surface Preparation", "Clean Up", ], }, { id: 6, name: "Carpet Cleaning",
price: 85, time_required: "2 hours", description: "Deep carpet cleaning to remove stains, dirt, and
allergens.", image: "https://placehold.co/600x400?text=Carpet+Cleaning", features: ["Deep Cleaning",
"Stain Removal", "Deodorizing", "Quick Drying"], }, ]); // Top professionals for each service - in a
real app, this would come from an API const professionals = ref([ { id: 1, name: "John Smith",
service_id: 1, rating: 4.8, reviews: 56 }, { id: 2, name: "Maria Garcia", service_id: 1, rating:
4.7, reviews: 42 }, { id: 3, name: "Robert Johnson", service_id: 2, rating: 4.9, reviews: 78 }, {
id: 4, name: "Sarah Lee", service_id: 3, rating: 4.6, reviews: 31 }, { id: 5, name: "James Wilson",
service_id: 4, rating: 4.8, reviews: 65 }, { id: 6, name: "Emily Brown", service_id: 5, rating: 4.9,
reviews: 89 }, { id: 7, name: "Michael Davis", service_id: 6, rating: 4.7, reviews: 47 }, ]); //
Selected service for details const selectedService = ref(null); const showServiceDetails =
ref(false); // Search and filter functionality const searchTerm = ref(""); const location = ref("");
const minPrice = ref(""); const maxPrice = ref(""); // Locations for dropdown const locations = [ {
value: "new-york", label: "New York" }, { value: "los-angeles", label: "Los Angeles" }, { value:
"chicago", label: "Chicago" }, { value: "houston", label: "Houston" }, { value: "phoenix", label:
"Phoenix" }, ]; const filteredServices = computed(() => { return services.value.filter((service) =>
{ // Apply search term filter if ( searchTerm.value &&
!service.name.toLowerCase().includes(searchTerm.value.toLowerCase()) && !service.description
.toLowerCase() .includes(searchTerm.value.toLowerCase()) ) { return false; } // Apply price filters
if (minPrice.value && service.price < Number.parseInt(minPrice.value)) { return false; } if
(maxPrice.value && service.price > Number.parseInt(maxPrice.value)) { return false; } return true;
}); }); // View service details const viewServiceDetails = (service) => { selectedService.value =
service; showServiceDetails.value = true; }; // Get professionals for a service const
getServiceProfessionals = (serviceId) => { return professionals.value.filter((p) => p.service_id ===
serviceId); }; // Book a service const bookService = (serviceId) => { // Use serviceId to pass to
the requests page (in a real app, this might store it in state) console.log(`Booking service with
ID: ${serviceId}`); router.push({ path: "/customer/requests", query: { service_id: serviceId }, });
};
