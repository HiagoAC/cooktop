import { v4 as uuidv4 } from 'uuid';
import { Button, Col, Form, InputGroup, Row, Stack } from 'react-bootstrap';
import { ReactElement, useEffect, useState } from 'react';
import { Badge } from './Badge';
import { Ingredient } from '../data/recipe_detail';
import '../styles/IngredientTagInputRow.css';


interface Props {
    ingredients?: Ingredient[],
    tags?: string[]
}

export function IngredientTagInputRow({ingredients, tags}: Props) {
    const [formTag, setFormTag] = useState<string>('');
    const [addedTags, setAddedTags] = useState<ReactElement[]>([]);
    const [formIngredient, setFormIngredient] = useState<string>('');
    const [addedIngredients, setAddedIngredients] = useState<ReactElement[]>([]);


    const addTagBadge = (tag: string): void => {
        const badge = <Badge
            item={tag}
            withDeleteButton={true}
            onDelete={deleteTagBadge}
            key={uuidv4()}
        />;
        setAddedTags(prevBadges => [...prevBadges, badge]);
        setFormTag('');
    };

    const deleteTagBadge = (item: string): void => {
        setAddedTags(prevBadges => {
            return prevBadges.filter(badge => badge.props.item !== item);
        });
    };

    const addIngredientBadge = (ingredient: string): void => {
        const badge = <Badge
            item={ingredient}
            withDeleteButton={true}
            onDelete={deleteIngredientBadge}
            key={uuidv4()}
        />;
        setAddedIngredients(prevBadges => [...prevBadges, badge]);
        setFormIngredient('');
    };

    const deleteIngredientBadge = (item: string): void => {
        setAddedIngredients(prevBadges => {
            return prevBadges.filter(badge => badge.props.item !== item);
        });
    };

    useEffect(() => {
        if (tags) {
            tags.forEach(tag => {
                addTagBadge(tag);
            })
        }
    
        if (ingredients) {
            ingredients.forEach(ingredient => {
                addIngredientBadge(ingredient.name);
            })
        }
    }, []);

    return (
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
                        <Button variant="outline-secondary" onClick={() => addIngredientBadge(formIngredient)}>
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
                        <Button variant="outline-secondary" onClick={() => addTagBadge(formTag)}>
                            + 
                        </Button>
                    </InputGroup>
                    <Stack direction="horizontal" gap={1} className="mt-2 custom-stack">
                        {addedTags}
                    </Stack>
                </Form.Group>
            </Col>
        </Row>
    )
}
