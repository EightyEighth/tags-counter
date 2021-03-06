import React, { useState, useEffect, useRef } from 'react';
import { Row, Container} from "react-bootstrap";

import UrlForm from '../../components/UrlForm';
import Chart from "../../components/TagCharts";

const URL_REGEX = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/;

const UrlCheck = props => {
  const [isValid, setValid] = useState(true);
  const [stateUrl, setUrl] = useState('');
  const [data, setData] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [delay, setDelay] = useState(1000);
  
  
  const getUrlData = () => {
    if (stateUrl) {
      fetch(process.env.REACT_APP_API_URL + `?url=${stateUrl}`)
          .then(response => response.json())
          .then(data => {
            const preparedData = Object.keys(data.tags).map((key) => {
              return {x: key, y: data.tags[key]}
            });
            setData(preparedData);
          }).catch(error => setValid(false));
      setIsRunning(!isRunning);
    }
  };
  
  useInterval(getUrlData, isRunning ? delay : null);
  
  const handlerCheckUrl = event => {
    const url = event.target.value;
    if (URL_REGEX.test(url)) {
      setUrl(url);
    }
    setValid(URL_REGEX.test(url));
  };
  
  const handleSubmit = event => {
    if (!isValid || !stateUrl) {
      event.preventDefault();
      event.stopPropagation();
      setValid(!isValid);
    }else{
       event.preventDefault();
    fetch(process.env.REACT_APP_API_URL, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: stateUrl})
    }).then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.log(error));
    setIsRunning(!isRunning);
    }

  };
  
  return (
      <React.Fragment>
        <Container>
          <Row className='justify-content-md-center'>
            <Chart color='#32a852' sampleData={data} title='Tags count'/>
          </Row>
          <Row className='justify-content-md-center'>
            <UrlForm
                isValid={isValid}
                isInvalid={!isValid}
                onClick={handleSubmit}
                onCheck={handlerCheckUrl}/>
          </Row>
        </Container>
      </React.Fragment>
  )
};

export default UrlCheck;

const useInterval = (callback, delay) => {
  const savedCallback = useRef();
  
  useEffect(() => {
    savedCallback.current = callback;
  });
  
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
};
