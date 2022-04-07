import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {ListGroup} from "react-bootstrap";

function Reserve(){


    const [choices, setChoices] = useState([])
    const [stops, changeStops] = useState({})
    const [mapURL, changeMapURL] = useState("")
    const [distance, changeDistance] = useState();
    const [duration, changeDuration] = useState();
    const stopsURL = "http://localhost:5000/getStops"



    function handleClick(event){
        const new_id = event.target.getAttribute("id");
        setChoices(choices => [...choices, new_id]);
    }

    function handleSubmit(){
        axios.post('http://localhost:5000/getPath', {choices}).then((res) =>{
            changeMapURL(res.data.map_url);
            changeDistance(res.data.distance);
            changeDuration(res.data.duration);
            console.log(res)
        } )
    }

    function convertHMS(value) {
    const sec = parseInt(value, 10);
    let hours   = Math.floor(sec / 3600); 
    let minutes = Math.floor((sec - (hours * 3600)) / 60); 
    let seconds = sec - (hours * 3600) - (minutes * 60); 
    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds; // Return is HH : MM : SS
    }

    useEffect(() =>{
    axios.get(stopsURL).then((res) =>{
        changeStops(res.data);
    });
    }, [])
    return(
        <div>
            <h1>Select stops</h1>
            {Object.entries(stops).length > 0 &&
    Object.entries(stops).map(([key, value]) => {
       return (
            <ListGroup key= {key} as="ul">
                <ListGroup.Item id={key} onClick={(e) => {
                    handleClick(e);
                }}>
                    {value}
                </ListGroup.Item>
            </ListGroup>
            
       );
  })}

            <button onClick={handleSubmit}>Submit</button>
            <img src={mapURL} alt="Map"></img>
            {duration > 0? <p> Duration: {convertHMS(duration)} </p> : ""}
            {distance > 0? <p> Distance: {distance/1000}km</p> : ""}
        </div>

        
    );
}

export default Reserve;