import React, { Component } from "react";
import { Grid, Typography, Button } from "@material-ui/core";

export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
        votesToSkip: 2,
        guestCanPause: false,
        isHost: false,
    };
    this.roomCode = this.props.match.params.roomCode;
    this.getRoomDetail()
  }

  getRoomDetail() {
      fetch('/api/get-room' + '?code=' + this.roomCode).then((response) => response.json()).then((data) => {
          this.setState({
              votesToSkip: data.votes_to_skip,
              guestCanPause: data.guest_can_pause,
              isHost: data.is_host,
          })
      })
  }

  render() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align='center'>
          <Typography variant='h4' component='h4'>
            {this.roomCode}
          </Typography>
        </Grid>
        <Grid item xs={12} align='center'>
          <p>Votes: {this.state.votesToSkip}</p>
        </Grid>
        <Grid item xs={12} align='center'>
          <p>Guest Can Pause: {this.state.guestCanPause.toString()}</p>
        </Grid>
        <Grid item xs={12} align='center'>
          <p>Host: {this.state.isHost.toString()}</p>
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="secondary" onClick={this.leaveRoomButtonPressed}>
            Leave Room
          </Button>
        </Grid>
      </Grid>
      )
    ;
  }

  leaveRoomButtonPressed = () => {
		const requestOptions = {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: '',
		};
		fetch('/api/leave-room', requestOptions)
			.then((response) => {
				this.props.history.push('/');
			})
			.catch((error) => {
				console.log(error);
			})
	}
}