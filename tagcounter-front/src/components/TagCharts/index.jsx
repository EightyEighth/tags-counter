import React from 'react';
import PropTypes from 'prop-types';
import { VictoryBar, VictoryChart, VictoryTheme, VictoryLabel, VictoryAxis, VictoryContainer } from "victory";


const Chart = props => {
  const { title, sampleData, width, height } = props;
  return(
      <div>
        <h3>{title}</h3>
        {sampleData.length ?
            <VictoryChart
                theme={VictoryTheme.material}
                horizontal
                padding={{ left: 80, right: 100 , top: 80, bottom: 80}}
                width={width ? width: 1000}
                height={height ? height: 1000}
                animate={{duration: 500}}>
              <VictoryAxis
                  orientation="left"
                  style={{
                    tickLabels: {
                      fontSize: 18
                    },
                    padding: 20,
                  }}
              />
              <VictoryBar
                  data={sampleData.length ? sampleData : [{}]}
                  style={{ labels: { fill: "black", fontSize: 15} }}
                  labels={d => Math.round(d.y)}
                  labelComponent={<VictoryLabel />}
                  
              />
            </VictoryChart>: ''}
      </div>
  )
};

Chart.propTypes = {
  title: PropTypes.string,
  data: PropTypes.array,
  color: PropTypes.string
};

export default Chart;
