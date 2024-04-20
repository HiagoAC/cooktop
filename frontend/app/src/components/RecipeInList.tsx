import { Link } from 'react-router-dom';
import { Card } from 'react-bootstrap';
import { BadgeStack } from './BadgeStack';
import styles from '../styles/RecipeInList.module.css';
import clockIcon from '../assets/clock_icon.svg';
import { useEffect, useState } from 'react';
import { downloadImage } from '../api/recipesApi';


interface Props {
    id: number,
    title: string,
    time_minutes: number,
    tags: string[],
}


export function RecipeInList({ id, title, time_minutes, tags }:
    Props) {
        const [imageSrc, setImageSrc] = useState<string>('');

        useEffect(() => {
            const fetchImage = async () => {
                downloadImage(String(id)).then(res => {
                    if (res.status === 200) {
                            const url: string = URL.createObjectURL(res.data);
                            setImageSrc(url);
                    } else {
                        console.log('Failed to fetch image');
                    }
                });
            };
            fetchImage();
        }, [id]);

        return <Card className={`${styles.recipe_card_container}`}>
            <Card.Img
                variant="top"
                src={imageSrc}
                height="150px"
                className={`${styles.card_img}`}
            />
            <Card.Body className="d-flex flex-column" key={id}>
                <Card.Title>{title}</Card.Title>
                <Card.Text>
                    <span>
                        <div className={`${styles.icon_container}`}>
                            <img
                                src={clockIcon}
                                alt="prep time"
                                className={`${styles.clock_icon}`}
                            />
                        </div> {time_minutes} min
                    </span>
                    <BadgeStack items={tags} />
                </Card.Text>
                <Link to={`/recipes/${id.toString()}`} className="stretched-link" />
            </Card.Body>
        </Card>
}
