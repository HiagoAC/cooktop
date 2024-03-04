import { useState } from 'react';
import { Alert, Button, Col, Form, Modal, Row } from 'react-bootstrap';
import { changePassword } from '../api/usersApi';


interface Props {
    show: boolean;
    handleClose: () => void;
}

export function ChangePasswordModal({show, handleClose}: Props) {
    const [currentPassword, setCurrentPassword] = useState<string>('');
    const [newPassword, setNewPassword] = useState<string>('');
    const [
        changePasswordSuccess,
        setChangePasswordSuccess
    ] = useState<boolean | null>(null);

    const handleCurrentPasswordChange = (
        event: React.ChangeEvent<HTMLInputElement>) => {
        setCurrentPassword(event.target.value);
    }

    const handleNewPasswordChange = (
        event: React.ChangeEvent<HTMLInputElement>) => {
        setNewPassword(event.target.value);
    }

    const handleSubmit = async () => {
            changePassword({
                old_password: currentPassword,
                new_password: newPassword
            }).then(res => {
                if (res.status === 204) {
                    setChangePasswordSuccess(true);
                } else {
                    setChangePasswordSuccess(false);
                }
            }).catch (_error => {
                setChangePasswordSuccess(false);
            })
    }

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{'Change Password'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                { changePasswordSuccess? (
                    <Alert variant="success" className="m-4">
                        {'Password changed!'}
                    </Alert>
                ) : changePasswordSuccess === false? (
                    <Alert variant="danger" className="mb-4">
                        {'Request failed.'}
                    </Alert>
                ) : (<></>)}
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
                <Button
                    className="custom_button"
                    onClick={handleSubmit}
                >
                    {'Change Password'}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}
