import { Col, Form, Row } from 'react-bootstrap';


interface Props {
    cookings: number;
    servings: number;
    setCookings: (value: number) => void;
    setServings: (value: number) => void;
}

export function UserPreferencesFormFields(
    {cookings, servings, setCookings, setServings}: Props) {

    const handleCookingsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setCookings(Number(event.target.value));
    };

    const handleServingsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setServings(Number(event.target.value));
    };

    return (
        <Row>
            <Col>
                <Form.Group>
                    <Form.Label>
                        {'How many times a week do you usually to cook?'}
                    </Form.Label>
                    <Form.Control
                        type="number"
                        min={1}
                        max={7}
                        value={cookings}
                        onChange={handleCookingsChange}
                    />
                </Form.Group>
            </Col>
            <Col>
                <Form.Group>
                    <Form.Label>
                        {'How many servings do you usually cook each time?'}
                    </Form.Label>
                    <Form.Control
                        type="number"
                        min={1}
                        value={servings}
                        onChange={handleServingsChange}
                    />
                </Form.Group>
            </Col>
        </Row>
    )
}
