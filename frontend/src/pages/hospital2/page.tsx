import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface Hospital {
  id: number;
  name: string;
  image?: string;
}

export default function SuperadminHospitalPage() {
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    username: "",
    email: "",
    password: "",
  });

  const navigate = useNavigate();

  // Fetch hospitals
  useEffect(() => {
    const fetchHospitals = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch("http://localhost:8000/hospitals/g", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) {
          throw new Error("Failed to fetch hospitals");
        }

        const data = await res.json();
        setHospitals(data);
      } catch (err) {
        console.error(err);
        setHospitals([]); // fallback to empty
      }
    };

    fetchHospitals();
  }, []);

  // Form input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Create hospital
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    try {
      const res = await fetch("http://localhost:8000/hospitals/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (res.ok) {
        setHospitals([
          ...hospitals,
          { id: data.hospital_id, name: formData.name, image: "" },
        ]);
        setFormData({ name: "", username: "", email: "", password: "" });
        setShowModal(false);
      } else {
        alert(data.detail || data.msg || "Error creating hospital");
      }
    } catch (err) {
      console.error(err);
      alert("Error creating hospital");
    }
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Hospitals</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Create Hospital
        </button>
      </div>

      {/* Cards or Empty State */}
      {hospitals.length === 0 ? (
        <div className="text-center text-gray-500">
          <p>No hospitals found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {hospitals.map((hospital) => (
            <div
              key={hospital.id}
              className="bg-white shadow rounded cursor-pointer hover:shadow-lg"
              onClick={() => navigate(`/hospital/${hospital.id}`)}
            >
              <img
                src={hospital.image || "https://via.placeholder.com/300x150"}
                alt={hospital.name}
                className="w-full h-36 object-cover"
              />
              <div className="p-4">
                <h3 className="font-bold text-lg">{hospital.name}</h3>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded shadow-lg w-96 relative">
            <button
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
              onClick={() => setShowModal(false)}
            >
              ✖
            </button>
            <h2 className="text-xl font-bold mb-4">Create Hospital</h2>
            <form onSubmit={handleSubmit} className="space-y-3">
              <input
                type="text"
                name="name"
                placeholder="Hospital Name"
                value={formData.name}
                onChange={handleChange}
                className="w-full p-2 border rounded"
                required
              />
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                className="w-full p-2 border rounded"
                required
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                className="w-full p-2 border rounded"
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                className="w-full p-2 border rounded"
                required
              />
              <button
                type="submit"
                className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
              >
                Create
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
