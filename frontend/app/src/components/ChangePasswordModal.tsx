import { useState } from 'react';
import { Button, Col, Form, Modal, Row } from 'react-bootstrap';


interface Props {
    show: boolean;
    handleClose: () => void;
}

export function ChangePasswordModal({show, handleClose}: Props) {
    const [currentPassword, setCurrentPassword] = useState<string>('');
    const [newPassword, setNewPassword] = useState<string>('');

    const handleCurrentPasswordChange = (
        event: React.ChangeEvent<HTMLInputElement>) => {
        setCurrentPassword(event.target.value);
    }

    const handleNewPasswordChange = (
        event: React.ChangeEvent<HTMLInputElement>) => {
        setNewPassword(event.target.value);
    }

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{'Change Password'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form className="p-3">
                    <Row>
                        <Col>
                            <Form.Group className="mb-3" controlId="currentPassword">
                                <Form.Label>{'Current Password'}</Form.Label>
                                <Form.Control
                                    type="password"
                                    placeholder="Current Password"
                                    value={currentPassword}
                                    onChange={handleCurrentPasswordChange}
                                />
                            </Form.Group>
                        </Col>
                        <Col>
                            <Form.Group className="mb-3" controlId="newPassword">
                                <Form.Label>{'New Password'}</Form.Label>
                                <Form.Control
                                    type="password"
                                    placeholder="New Password"
                                    value={newPassword}
                                    onChange={handleNewPasswordChange}
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button className="custom_button">
                    {'Change Password'}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}
