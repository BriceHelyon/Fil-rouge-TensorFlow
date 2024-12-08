import React, { useEffect, useState } from "react";
import { useNavigate, Outlet } from "react-router-dom";
import env from "../environment";

function ProtectedRoute() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true); 
    const [isAuthenticated, setIsAuthenticated] = useState(false); 

   
    const getCookie = (name) => {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    };

    useEffect(() => {
        const checkToken = async () => {
          
            const token = getCookie('authToken');
            if (!token) {
                navigate('/login');
                return;
                
            }

            
            const url = env.REACT_APP_PSQL_HOST + 'token'
            const data = { token: token };

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    const result = await response.json();
                    if (result.status == 200) {
                        setIsAuthenticated(true); 
                    } else {
                        navigate('/login');
                    }
                } else {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
            } catch (error) {
                console.error('Error:', error);
                navigate('/login'); 
            } finally {
                setLoading(false); 
            }
        };

        checkToken();
    }, [navigate]);

    if (loading) {
        return <div>Loading...</div>; 
    }

    return isAuthenticated ? <Outlet /> : null; 
}

export default ProtectedRoute;
