import { Button, Col, Form, Modal, Row } from 'react-bootstrap';
import { UserPreferencesFormFields } from './UserPreferencesFormFields';
import { createUser } from '../api/usersApi';
import { useState } from 'react';


interface Props {
    show: boolean;
    handleClose: () => void;
}


export function SignUpModal({show, handleClose}: Props) {
    const [firstName, setFirstName] = useState<string>('');
    const [lastName, setLastName] = useState<string>('');
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    const handleCreateUser = () => {
        createUser({
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password
        });

        handleClose();
    };
  
    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{'Sign Up'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Row>
                        <Col>
                            <Form.Group className="mb-3" controlId="firstName">
                                <Form.Label>{'First Name'}</Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder="First Name"
                                    value={firstName}
                                    onChange={
                                        (e) => setFirstName(e.target.value)}
                                />
                            </Form.Group> 
                        </Col>
                        <Col>
                            <Form.Group className="mb-3" controlId="lastName">
                                <Form.Label>{'Last Name'}</Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder="Last Name"
                                    value={lastName}
                                    onChange={
                                        (e) => setLastName(e.target.value)}
                                />
                            </Form.Group> 
                        </Col>
                    </Row>
                    <Form.Group className="mb-3" controlId="emailAddress">
                        <Form.Label>{'Email'}</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Email"
                            value={email}
                            onChange={
                                (e) => setEmail(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="password">
                        <Form.Label>{'Password'}</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={
                                (e) => setPassword(e.target.value)}
                        />
                    </Form.Group>
                    <UserPreferencesFormFields />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button
                    className="custom_button"
                    onClick={handleCreateUser}
                >
                    {'Create Account'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
