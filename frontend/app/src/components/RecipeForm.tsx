import { Button, Col, Form, InputGroup, Row, Stack } from 'react-bootstrap';
import { ReactElement, useState } from 'react';
import { Badge } from './Badge';
import '../styles/RecipeForm.css';


export function RecipeForm() {
    const [formTag, setFormTag] = useState<string>('');
    const [addedTags, setAddedTags] = useState<ReactElement[]>([]);
    const [formIngredient, setFormIngredient] = useState<string>('');
    const [addedIngredients, setAddedIngredients] = useState<ReactElement[]>([]);

    const addTagBadge = (): void => {
        const badge = <Badge item={formTag} withDeleteButton={true} />;
        setAddedTags(prevBadges => [...prevBadges, badge]);
        setFormTag('');
    };

    const addIngredientBadge = (): void => {
        const badge = <Badge item={formIngredient} withDeleteButton={true} />;
        setAddedIngredients(prevBadges => [...prevBadges, badge]);
        setFormIngredient('');
    };

    return (
        <Form className="p-3">
            <Form.Group className="mb-3" controlId="addFromURL">
                <Form.Label>Add Recipe from URL</Form.Label>
                <Form.Control type="url" placeholder="type a URL" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="title">
                <Form.Label>Title</Form.Label>
                <Form.Control type="text" placeholder="Title" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="description">
                <Form.Label>Description</Form.Label>
                <Form.Control as="textarea" rows={2} placeholder="Description" />
            </Form.Group>
            <Row md={2} xs={1}>
                <Col>
                    <Form.Group className="mb-3" controlId="prepTime">
                        <Form.Label>Preparation Time</Form.Label>
                        <InputGroup>
                            <Form.Control type="number" placeholder="Preparation Time" />
                            <InputGroup.Text>minutes</InputGroup.Text>
                        </InputGroup>
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3" controlId="recipeType">
                        <Form.Label>Type</Form.Label>
                        <Form.Select aria-label="Default select example">
                            <option>Recipe Type</option>
                            <option value="mai">main dish</option>
                            <option value="sid">side dish</option>
                            <option value="sal">salad</option>
                            <option value="des">dessert</option>
                            <option value="sna">snack</option>
                        </Form.Select>
                    </Form.Group>
                </Col>
            </Row>
            <Row  md={2} xs={1}>
                <Col>
                    <Form.Group className="mb-3" controlId="ingredients">
                        <Form.Label>Ingredients</Form.Label>
                        <InputGroup>
                            <Form.Control
                                type="text"
                                placeholder="Type a new ingredient and press add."
                                value={formIngredient}
                                onChange={(e) => setFormIngredient(e.target.value)}
                            />
                            <Button variant="outline-secondary" onClick={() => addIngredientBadge()}>
                                 + 
                            </Button>
                        </InputGroup>
                        <Stack direction="horizontal" gap={1} className="mt-2 custom-stack">
                            {addedIngredients}
                        </Stack>
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3" controlId="tags">
                        <Form.Label>Tags</Form.Label>
                        <InputGroup>
                            <Form.Control
                                    type="text"
                                    placeholder="Type a new tag and press add."
                                    value={formTag}
                                    onChange={(e) => setFormTag(e.target.value)}
                            />
                            <Button variant="outline-secondary" onClick={() => addTagBadge()}>
                                 + 
                            </Button>
                        </InputGroup>
                        <Stack direction="horizontal" gap={1} className="mt-2 custom-stack">
                            {addedTags}
                        </Stack>
                    </Form.Group>
                </Col>
            </Row>
        </Form>
    )
}
