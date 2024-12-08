import React, { useState, useEffect } from 'react';
import img from '../assets/img/image_inscription.png';
import CryptoJS from 'crypto-js';
import env from '../environment';
import { useNavigate } from 'react-router-dom';
 
 
function Login() {
 
    const navigate = useNavigate()
  
    const [mail, setMail] = useState("")
    const [password, setPassword] = useState("")
    const [cryptedPassword, setCryptedPassword] = useState("")
    const [isSubmitted, setIsSubmitted] = useState(false)
    const [showError, setShowError] = useState(false)
    const [showFormatError, setShowFormatError] = useState(false)
 
    const mailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    useEffect(() => {
        
        const token = getCookie('authToken')

        if(token) {
            logout(token)
        }
       
    }, []); 

    const getCookie = (name) => {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    };

    const deleteCookie = (name) => {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    };

    const logout = async (token) => {

       
        const url = env.REACT_APP_PSQL_HOST + 'logout/' + token

 
        try {
            const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
            });
 
            if (response.ok) {
                const result = await response.json();
                console.log('Success:', result);

                if(result.status == 200) {
                    console.log('disconnected')
                    deleteCookie('authToken')
                }

       
            }
            else {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
 
        } catch (error) {
            console.error('Error:', error);
        }
       
    }
 
    const checkMail = (mail) => {
        return mailRegex.test(mail)
    }
 
    function hashPassword(password) {
        return CryptoJS.SHA512(password).toString(CryptoJS.enc.Hex);
    }
 
    const handleSubmit = () => {
        setIsSubmitted(true)
 
        if(checkMail(mail.trim())) {
            setShowFormatError(false)
            setCryptedPassword(hashPassword(password))
        }
        else {
            setShowFormatError(true)
            setShowError(false)
        }
       
    }
 
    const checkLogin = async () => {
        if (!cryptedPassword) return;
        
        const url = env.REACT_APP_PSQL_HOST + 'login'
        console.log(url)
        const data = {
            "email": mail.trim(),
            "password": cryptedPassword,
        };
 
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
                console.log('Success:', result);
   
                if(result.status == 200) {
                  setShowError(false)
                  const tokenValue = result.access_token;
 
 
                  const date = new Date();
                  date.setTime(date.getTime() + (12 * 60 * 60 * 1000));
                  const expires = "; expires=" + date.toUTCString();
 
   
                  document.cookie = "authToken=" + tokenValue + expires + "; path=/";
 
                  navigate('/')
                }
                else if(result.status == 403) {
                    setShowError(true)
                }
       
            }
            else {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
 
        } catch (error) {
            console.error('Error:', error);
        }
    }
 
    useEffect(() => {
        if (cryptedPassword) {
          checkLogin()
        }
      }, [cryptedPassword]);
 
 
    return(
        <div className='body-container'>
              <div className="login-container">
            <img src={img} className='img' ></img>
            <div className="form">
                <h1>Connexion</h1>
                <div className='field'>
                    <input type="text" name="email" placeholder="Email" onChange={(e) => setMail(e.target.value) } value={mail}></input>
                </div>
                <div className='field'>
                    <input type="password" name="password" placeholder="Mot de passe"  onChange={(e) => setPassword(e.target.value)} value={password}></input>
                    {showFormatError && isSubmitted && <span className='error'>Formats incorrects</span>}
                    {showError && isSubmitted && <span className='error'>L'email ou le passe est incorrect</span>}
                </div>
 
               
             
                <button type="button" className="btn" onClick={() => handleSubmit()}>Se connecter</button>
            </div>
        </div>
        </div>
      
    )
}
 
export default Login