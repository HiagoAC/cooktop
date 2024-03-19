import { v4 as uuidv4 } from 'uuid';
import { Button, Form, InputGroup, Stack } from 'react-bootstrap';
import { ReactElement, useEffect, useState } from 'react';
import { Badge, Props as BadgeProps } from './Badge';
import styles from '../styles/BadgeStackFormGroup.module.css';


interface Props {
    items: string[];
    setItems: (items: string[]) => void;
    label: string;
    placeholder: string
}


export function BadgeStackFormGroup({items, setItems, label, placeholder}: Props) {
    const [formItem, setFormItem] = useState<string>('');
    const [addedItems, setAddedItems] = useState<ReactElement[]>([]);

    const addBadge = (item: string): void => {
        const badge = <Badge
            item={item}
            onDelete={deleteBadge}
            key={uuidv4()}
        />;
        setAddedItems(prevBadges => [...prevBadges, badge]);
        setItems([...items, item]);
        setFormItem('');
    };

    const deleteBadge = (item: string): void => {
        setAddedItems(prevBadges => {
            return prevBadges.filter(
                badge => (badge.props as BadgeProps).item !== item);
        });
        const updatedItems = items.filter(i => i !== item);
        setItems(updatedItems);
    };

    useEffect(() => {
        items.forEach(item => {
            addBadge(item);
        })
    }, []);

    return (
        <Form.Group className="mb-3" controlId="tags">
            <Form.Label>{label}</Form.Label>
            <InputGroup>
                <Form.Control
                        type="text"
                        placeholder={placeholder}
                        value={formItem}
                        onChange={(e) => setFormItem(e.target.value)}
                />
                <Button variant="outline-secondary" onClick={() => addBadge(formItem)}>
                    + 
                </Button>
            </InputGroup>
            <Stack direction="horizontal" gap={1} className={`mt-2  ${styles.custom_stack}`}>
                {addedItems}
            </Stack>
        </Form.Group>
    )
}
